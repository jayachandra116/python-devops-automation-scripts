import logging
from utils.logger import get_logger


def test_logger_creation():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
