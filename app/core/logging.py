"""
Logging Configuration Module

Configures structured logging
for the application.
"""

import structlog

from logging.config import (
    dictConfig
)

from app.core.config import (
    settings
)


def setup_logging():
    """
    Configure structured logging
    for the application.
    """

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": (
                        "%(asctime)s | "
                        "%(levelname)s | "
                        "%(name)s | "
                        "%(message)s"
                    )
                },
            },
            "handlers": {
                "console": {
                    "class": (
                        "logging.StreamHandler"
                    ),
                    "formatter": (
                        "standard"
                    ),
                    "level": (
                        settings.log_level
                    ),
                },
            },
            "root": {
                "handlers": [
                    "console"
                ],
                "level": (
                    settings.log_level
                ),
            },
        }
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(
                fmt="iso"
            ),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=(
            structlog.stdlib.BoundLogger
        ),
        context_class=dict,
        logger_factory=(
            structlog.stdlib.LoggerFactory()
        ),
        cache_logger_on_first_use=True,
    )


setup_logging()

# Default application logger
logger = structlog.get_logger(
    "deepcontext"
)

# Logger factory
get_logger = structlog.get_logger