import logging
from pathlib import Path


def get_logger(name: str, log_file: str = "logs/devops.log") -> logging.Logger:
    """Returns a configured logger.

    Args:
        name (str): Name of the logger
        log_file (str, Optional):
            File name to store the logs.
            Defaults to 'logs/devops.log'

    Returns:
        logging.Logger: Configured logger to use
    """
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
