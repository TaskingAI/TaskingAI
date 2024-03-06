import os
import logging

# Retrieve the log level from the environment variables (defaulting to INFO).
log_level = os.environ.get("LOG_LEVEL", "INFO")

__all__ = ["init_logger"]


def init_logger():
    # Create a logger object.
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Configure the log handler and format.
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create a console handler.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
