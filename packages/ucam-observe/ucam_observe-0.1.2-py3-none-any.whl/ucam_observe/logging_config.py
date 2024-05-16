import os
from logging.config import dictConfig

import structlog


def get_log_level():
    """Retrieve log level from environment variables."""
    return os.getenv("LOG_LEVEL", "INFO").upper()


def get_console_logging_status():
    """Retrieve console logging status from environment variables."""
    return os.getenv("CONSOLE_LOGGING", "False").lower() in ("true", "1")


def configure_logging():
    """Configure structured logging for both Python logging and structlog."""

    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.render_to_log_kwargs,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "console": {
                    "()": "structlog.stdlib.ProcessorFormatter",
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                },
                "json": {
                    "()": "structlog.stdlib.ProcessorFormatter",
                    "processor": structlog.processors.JSONRenderer(),
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                },
                "json": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console" if get_console_logging_status() else "json"],
                    "level": get_log_level(),
                    "propagate": True,
                },
            },
        }
    )
