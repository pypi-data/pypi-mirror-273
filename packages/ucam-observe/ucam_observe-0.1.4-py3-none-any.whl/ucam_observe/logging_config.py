import os
import re
from logging.config import dictConfig

import structlog


def get_log_level():
    """Retrieve log level from environment variables."""
    return os.getenv("LOG_LEVEL", "INFO").upper()


def get_console_logging_status():
    """Retrieve console logging status from environment variables."""
    return os.getenv("CONSOLE_LOGGING", "False").lower() in ("true", "1")


def _add_gcp_log_severity(logger, method_name, event_dict):  # pragma: no cover
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


# From https://albersdevelopment.net/2019/08/15/using-structlog-with-gunicorn/
def _gunicorn_combined_logformat(logger, name, event_dict):
    if event_dict.get("logger") == "gunicorn.access":
        try:
            message = event_dict["event"]

            parts = [
                r"(?P<host>\S+)",  # host %h
                r"\S+",  # indent %l (unused)
                r"(?P<user>\S+)",  # user %u
                r"\[(?P<time>.+)\]",  # time %t
                r'"(?P<request>.+)"',  # request "%r"
                r"(?P<status>[0-9]+)",  # status %>s
                r"(?P<size>\S+)",  # size %b (careful, can be '-')
                r'"(?P<referer>.*)"',  # referer "%{Referer}i"
                r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
            ]
            pattern = re.compile(r"\s+".join(parts) + r"\s*\Z")
            m = pattern.match(message)
            res = m.groupdict()

            if res["user"] == "-":
                res["user"] = None

            res["status"] = int(res["status"])

            if res["size"] == "-":
                res["size"] = 0
            else:
                res["size"] = int(res["size"])

            if res["referer"] == "-":
                res["referer"] = None

            event_dict.update(res)

        # We want the log even if this code fails
        except:  # noqa E722 rare occasion where we do want to carry on if this block fails
            pass

    return event_dict


def _set_process_id(_, __, event_dict):
    event_dict["process_id"] = os.getpid()
    return event_dict


def get_dict_config_formatters():
    return {
        "developer_console": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.dev.ConsoleRenderer(colors=True),
        },
        "json": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.TimeStamper(fmt="iso"),
                _add_gcp_log_severity,
                _gunicorn_combined_logformat,
                _set_process_id,
            ],
        },
    }


def get_dict_config():
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": get_dict_config_formatters(),
        "handlers": {
            "developer_console": {
                "class": "logging.StreamHandler",
                "formatter": "developer_console",
            },
            "json": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "loggers": {
            "": {
                "handlers": ["developer_console" if get_console_logging_status() else "json"],
                "level": get_log_level(),
                "propagate": True,
            },
        },
    }


def configure_structlog():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def configure_logging(force_reset=False):
    """Configure structured logging for both Python logging and structlog."""

    global configure_logging_run
    if not force_reset and configure_logging_run:
        return

    configure_logging_run = True

    configure_structlog()

    dictConfig(get_dict_config())


configure_logging_run = False
