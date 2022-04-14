import logging
from util.ClieckHouse import SingletonMetaClass

LOG_DEBUG_LEVEL = logging.DEBUG
LOG_INFO_LEVEL = logging.INFO
LOG_WARN_LEVEL = logging.WARNING
LOG_ERROR_LEVEL = logging.ERROR
LOG_DEFAULT_LEVEL = LOG_INFO_LEVEL


class PhLogging(object):

    def __init__(self):
        pass

    def phLogger(self, logger_name, level=LOG_DEFAULT_LEVEL):

        # root = logging.getLogger()
        # if root.handlers:
        #     for handler in root.handlers:
        #         root.removeHandler(handler)

        logging.basicConfig(level=level,
                            format="%(asctime)s %(name)s %(module)s %(levelname)s %(message)s",
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )

        logger = logging.getLogger(logger_name)

        return logger
