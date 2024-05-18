import structlog

from .logging_config import configure_logging


def get_structlog_logger(*args, **kwargs):
    configure_logging()

    """Get a logger with the specified name."""
    return structlog.get_logger(*args, **kwargs)
