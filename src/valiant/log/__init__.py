"""Logging for the Valiant system.

This is an initial logging setup and may be underwhelming.
"""
from copy import deepcopy
import logging
from logging.config import dictConfig
import sys
import structlog
from typing import Dict
from structlog.stdlib import LoggerFactory


"""A basic default that spits out to standard out."""
DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"standard": {"format": "%(message)s"}},
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


def setup_logging_configuration(
    disable_existing_loggers: bool = True,
    handlers: Dict = None,
    formatters: Dict = None,
    loggers: Dict = None,
) -> Dict:
    """Convenience function to structure the logging config.

    This method essentially layers over the top of the default config.

    See: https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
    See: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema

    Args:
        disable_existing_loggers: as per the configuration dictionary schema
        handlers: as per the configuration dictionary schema
        formatters: as per the configuration dictionary schema
        loggers: as per the configuration dictionary schema

    Returns:
        A ready-to-go logging config.
    """
    config = deepcopy(DEFAULT_CONFIG)
    config["disable_existing_loggers"] = disable_existing_loggers
    if handlers:
        config["handlers"] = handlers
    if formatters:
        config["formatters"] = formatters
    if loggers:
        config["loggers"] = loggers
    return config


def configure_logging(config: Dict = DEFAULT_CONFIG) -> None:
    """Configures logging for the application.

    This is called by Valiant.__init__

    See: https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig

    Args:
        config: A dictionary acceptable to logging.config.dictConfig
    """
    dictConfig(deepcopy(config))

    # See: http://www.structlog.org/en/stable/standard-library.html#rendering-within-structlog
    structlog.configure_once(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger():  # noqa:ANN201
    """Get a logger for your needs.

    Returns:
        An object that allows you to call standard logging methods
        but also pass in arbitrary keyword params (kwargs) that are
        put out to the log in a handy parseable form

    Example usage:

        from valiant.log import get_logger
        log = get_logger()

        log.info(
            f"SPDX reporter located {len(report.findings)} findings",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
            repository_url=package_metadata.repository_url,
        )
    """
    return structlog.get_logger()
