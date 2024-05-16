import structlog

from .logging_config import configure_logging

configure_logging()


def get_structlog_logger(name):
    """Get a logger with the specified name."""
    return structlog.get_logger(name)
