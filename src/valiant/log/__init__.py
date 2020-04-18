"""Logging for the Valiant system.

This is an initial logging setup and may be underwhelming.

Copyright (c) 2020 The Valiant Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from logging.config import dictConfig, fileConfig
from pathlib import Path
from typing import Dict, Optional


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
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO", "propagate": False}
    },  # root logger
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
    from copy import deepcopy

    config = deepcopy(DEFAULT_CONFIG)
    config["disable_existing_loggers"] = disable_existing_loggers
    if handlers:
        config["handlers"] = handlers
    if formatters:
        config["formatters"] = formatters
    if loggers:
        config["loggers"] = loggers
    return config


def configure_logging(
    dict_config: Dict = DEFAULT_CONFIG, file_config: Optional[Path] = None
) -> None:
    """Configures logging for the application.

    This is usually called by valiant.config.Config.__init__

    If a file_config is provided, the dict_config is ignored.

    If logging has already been configured further calls to this function will
    just be silently ignored.

    See: https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig

    Args:
        dict_config: A dictionary acceptable to logging.config.dictConfig
        file_config: Path to a logging config file - see
            https://docs.python.org/3/library/logging.config.html#logging-config-fileformat

    Raises:
        ValueError: When the file provided in file_config does not exist.
    """
    from copy import deepcopy
    import structlog
    from structlog.stdlib import LoggerFactory

    if structlog.is_configured():
        return

    if file_config:
        if not file_config.exists():
            raise ValueError(
                (
                    f"The logging configuration file does not exist: {file_config}."
                    f" CWD is {Path.cwd()}."
                )
            )
        fileConfig(file_config)
    else:
        dictConfig(deepcopy(dict_config))

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
    import structlog

    return structlog.get_logger()
