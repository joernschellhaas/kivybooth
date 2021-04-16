"""
Due to some oddities of Kivy logging, we need this module to 
  - Get Python logging to work normally
  - Have log messages created with Python logging formatted the same way as Kivy logging messages

It is important to import this module before any logger is retrieved from Python logging.
"""

# See https://stackoverflow.com/questions/36106353/using-python-logging-when-logging-root-has-been-redefined-kivy


import logging
import kivy.logger

logging.Logger.manager.root = kivy.logger.Logger
kivy.logger.Logger.setLevel(logging.DEBUG)


class KivyCompatLogger(logging.Logger):
    def _log(self, level, msg, args, **kwargs):
        super()._log(level, self.name + ": " + msg, args, **kwargs)

logging.setLoggerClass(KivyCompatLogger)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    for level in [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]:
        logger.log(level, "Test message on level %s", logging.getLevelName(level))
