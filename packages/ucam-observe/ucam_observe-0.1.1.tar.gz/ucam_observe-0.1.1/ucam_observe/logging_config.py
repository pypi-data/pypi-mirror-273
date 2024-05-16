import os
from logging.config import dictConfig

import structlog


def get_log_level():
    """Retrieve log level from environment variables."""
    return os.getenv("LOG_LEVEL", "INFO").upper()


def configure_logging():
    """Configure structured logging for both Python logging and structlog."""
    log_level = get_log_level()

    base_formatter = {
        "()": "structlog.stdlib.ProcessorFormatter",
        "processor": structlog.processors.JSONRenderer(),
    }

    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.render_to_log_kwargs,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    dictConfig(
        {
            "version": 1,
            "formatters": {"json": base_formatter},
            "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": True,
                },
            },
        }
    )
