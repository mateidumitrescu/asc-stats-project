"""This module contains the configuration for the logger."""

import logging
from logging.handlers import RotatingFileHandler
import time

class UTCFormatter(logging.Formatter):
    """This class is used to format the time in UTC."""

    def __init__(self, fmt=None, datefmt=None, style='%'):
        # initializing the formatter
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        # converter set to gmtime
        self.converter = time.gmtime

    def formatTime(self, record, datefmt=None):
        """Format the creation time of the record."""
        # getting the current time
        current_time = self.converter(record.created)

        # checking if datefmt is set
        if datefmt:
            # if so, format the time accordingly
            s = time.strftime(datefmt, current_time)
        else:
            try:
                # using the default date format
                s = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                s = "%s,%03d" % (s, record.msecs)
            except ValueError:
                s = "0000-00-00 00:00:00,000"
        return s

def setup_logger():
    """Function to setup the logger."""
    logger = logging.getLogger(__name__)
    # can now accept only info, warning, error, and critical messages
    logger.setLevel(logging.INFO)

    # file handler: maximum size of 1000 bytes and maximum of 5 log files
    handler = RotatingFileHandler('webserver.log',
                                  maxBytes=1000,
                                  backupCount=5
                                  )
    # formatter: date and time, log level, and the message
    formatter = UTCFormatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S %z')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
