import logging
import logging.config
import os.path

import click
import flask
import functions_framework
import gunicorn.app.base
import structlog
from cloudevents.http.event import CloudEvent
from gunicorn.config import get_default_config_file
from ucam_observe import get_structlog_logger
from werkzeug.exceptions import InternalServerError

from .exceptions import UCAMFAASException

logger = get_structlog_logger(__name__)


def _common_function_wrapper(function):
    def _common_function_wrapper_internal(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except UCAMFAASException as exception:
            exception_name = exception.__class__.__name__

            logger.warning("function_failed_gracefully", exception_name=exception_name)

            raise InternalServerError(description=f"The function raised {exception_name}.")

        except Exception as exception:
            exception_name = exception.__class__.__name__

            logger.error("function_failed_uncaught_exception", exception_name=exception_name)

            # FIXME dump stack trace into logs for unhandled exception

            raise exception

    return _common_function_wrapper_internal


def raw_event(function):
    @_common_function_wrapper
    def _raw_event_internal(request: flask.Request) -> flask.typing.ResponseReturnValue:
        return_value = function(request.data)

        if return_value is not None:
            return return_value

        return "", 200

    _raw_event_internal.__name__ = function.__name__
    _raw_event_internal = functions_framework.http(_raw_event_internal)

    _raw_event_internal.__wrapped__ = function

    return _raw_event_internal


def cloud_event(function):
    @_common_function_wrapper
    def _cloud_event_internal(event: CloudEvent) -> None:
        return function(event.data)

    _cloud_event_internal.__name__ = function.__name__
    _cloud_event_internal = functions_framework.cloud_event(_cloud_event_internal)

    _cloud_event_internal.__wrapped__ = function
    return _cloud_event_internal


class FaaSGunicornApplication(gunicorn.app.base.Application):
    _BASE_CONFIG = "/etc/gunicorn.conf.py"

    def __init__(self, app, host, port):
        self.host = host
        self.port = port
        self.app = app

        super().__init__()

    def load_config(self):
        if os.path.isfile(self._BASE_CONFIG):
            self.load_config_from_file(self._BASE_CONFIG)

        default_config = get_default_config_file()
        if default_config is not None:
            self.load_config_from_file(default_config)

        self.cfg.set("bind", f"{self.host}:{self.port}")

    def load(self):
        return self.app


def _add_log_severity(logger, method_name, event_dict):  # pragma: no cover
    """
    Add the log level to the event dict under the "severity" key.

    This is used as a structlog log processor, and is necessary as severity is used by GCP instead
    of level.

    Based on the structlog.stdlib.add_log_level processor.
    """
    if method_name == "warn":
        method_name = "warning"
    event_dict["severity"] = method_name
    return event_dict


def _configure_structlog():  # pragma: no cover
    """
    Internal function to configure structlog with a standard set of options.
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            _add_log_severity,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def _configure_logging(debug):  # pragma: no cover
    """
    Internal function to configure python logging with standard options, and integrate with
    structlog.
    """
    structlog_foreign_pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                # This formatter logs as structured JSON suitable for use in Cloud hosting
                # environments.
                "json_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                    "foreign_pre_chain": structlog_foreign_pre_chain,
                },
                # This formatter logs as coloured text suitable for use by humans.
                "console_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                    "foreign_pre_chain": structlog_foreign_pre_chain,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console_formatter",
                },
                "json": {
                    "class": "logging.StreamHandler",
                    "formatter": "json_formatter",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console" if debug else "json"],
                    "propagate": True,
                    "level": "INFO",
                },
            },
        }
    )


def _initialize_logging(debug):  # pragma: no cover
    """
    Internal function to initialise logging, configuring python logging and structlog.
    """
    _configure_structlog()
    _configure_logging(debug)
    logger = logging.getLogger()
    return logger.handlers[:], structlog.wrap_logger(logger)


def _initialize_ucam_faas_app(target, source, debug):
    handlers, logger = _initialize_logging(debug)
    app = functions_framework.create_app(target, source)
    app.logger.handlers = handlers

    @app.route("/healthy")
    @app.route("/status")
    def get_status():
        return "ok"

    return app


def run_ucam_faas(target, source, host, port, debug):  # pragma: no cover
    app = _initialize_ucam_faas_app(target, source, debug)
    if debug:
        app.run(host, port, debug)
    else:
        server = FaaSGunicornApplication(app, host, port)
        server.run()


@click.command()
@click.option("--target", envvar="FUNCTION_TARGET", type=click.STRING, required=True)
@click.option("--source", envvar="FUNCTION_SOURCE", type=click.Path(), default=None)
@click.option("--host", envvar="HOST", type=click.STRING, default="0.0.0.0")
@click.option("--port", envvar="PORT", type=click.INT, default=8080)
@click.option("--debug", envvar="DEBUG", is_flag=True)
def _cli(target, source, host, port, debug):  # pragma: no cover
    run_ucam_faas(target, source, host, port, debug)
