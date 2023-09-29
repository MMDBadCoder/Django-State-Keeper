import logging

from django.conf import settings


class LoggerFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if LoggerFactory.__instance is None:
            LoggerFactory.__instance = LoggerFactory.create_logger()
        return LoggerFactory.__instance

    @staticmethod
    def create_logger():
        log_level = logging.INFO
        if hasattr(settings, 'LOG_LEVEL'):
            log_level = settings.LOG_LEVEL
        # Create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(CustomLogFormatter())

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

        return logger


class CustomLogFormatter(logging.Formatter):
    white = '\x1b[38;5;255m'
    grey = "\x1b[38;20m"
    yellow = "\x1b[38;5;227m"
    red = "\x1b[38;5;9m"
    bold_red = "\x1b[31;1m"
    blue = '\x1b[38;5;45m'
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: white + format,
        logging.INFO: blue + format,
        logging.WARNING: yellow + format,
        logging.ERROR: red + format,
        logging.CRITICAL: bold_red + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
