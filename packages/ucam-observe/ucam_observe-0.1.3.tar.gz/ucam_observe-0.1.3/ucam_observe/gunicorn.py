from ucam_observe.logging_config import get_dict_config_formatters, get_log_level

logconfig_dict = {
    "formatters": get_dict_config_formatters(),
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            # Whilst True is the default in CONFIG_DEFAULTS within structlog, these default
            # settings cause duplicate logs (the default settings are only applied when
            # logconfig_dict is specified and is not empty), presumably because other
            # settings cause gunicorn to programmatically add stdout/err to these existing
            # handlers.
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
            "qualname": "gunicorn.access",
        },
    },
}

loglevel = get_log_level().lower()
