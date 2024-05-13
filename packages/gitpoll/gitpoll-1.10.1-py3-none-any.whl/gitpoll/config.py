# Logging
import os

LOGGER_NAME = "gitpoll"
MAX_LOG_SIZE = 1024 * 1024 * 1024  # 1GB

LOGGER_SET_LEVEL = os.getenv('GITPOLL_LOG_LEVEL', 'INFO')
# Optimized log format: Date-Time Level Module:Function Message
# Example: 01-01 00:00:00 INFO module:func message
LOGGER_FORMAT = "%(asctime)s %(levelname)s %(module)s:%(funcName)s %(message)s"
DATE_FORMAT = '%m-%d %H:%M:%S'
