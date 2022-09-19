import logging
from logging import Logger


def get_logger(name: str) -> Logger:
    if logging.getLogger().hasHandlers():
        # AWS Lambda preconfigures a handler
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
    return logging.getLogger(name)
