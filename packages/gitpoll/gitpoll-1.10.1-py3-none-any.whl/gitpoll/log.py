# gitpoll/log.py
import logging
import sys
from logging import StreamHandler, Formatter, getLogger, Logger
from logging.handlers import SysLogHandler

from . import config as _cfg


def get_logger() -> Logger:
    """Configure and retrieve a logger instance for the application."""
    logger = getLogger(_cfg.LOGGER_NAME)
    logger.setLevel(_cfg.LOGGER_SET_LEVEL)

    # stdout handler
    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(
        Formatter(_cfg.LOGGER_FORMAT, datefmt=_cfg.DATE_FORMAT)
    )
    logger.addHandler(console_handler)

    # I'll support syslog later
    #
    # if syslog:
    #    logger.addHandler(console_handler)
    #    # syslog handler
    #    syslog_handler = None
    #    if sys.platform == "linux":
    #        syslog_handler = SysLogHandler(address="/dev/log")
    #    elif sys.platform == "darwin":
    #        syslog_handler = SysLogHandler(address="/var/run/syslog")
    #    else:
    #        logger.warning(
    #            "Syslog address not found for platform: {}".format(
    #                sys.platform
    #            )
    #        )
    #
    #    if syslog_handler:
    #        syslog_handler.setFormatter(
    #            Formatter(_cfg.LOGGER_FORMAT, datefmt=_cfg.DATE_FORMAT)
    #        )
    #        logger.addHandler(syslog_handler)

    return logger


logger = get_logger()
