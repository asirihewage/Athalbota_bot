import logging
from logging import handlers


def log(message):
    formatter = logging.Formatter(
        '%(asctime)s * %(name)s * %(levelname)s * [%(filename)s:%(lineno)s  %(funcName)20s() ] %(message)s')
    logger = logging.getLogger()
    logHandler = handlers.TimedRotatingFileHandler('logs/logger.log', when='M', interval=53, backupCount=24)
    logHandler.setLevel(logging.ERROR)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.error(message)
