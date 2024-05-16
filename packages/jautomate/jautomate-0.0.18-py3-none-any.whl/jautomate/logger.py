"""
Sets up a log handlers.

Errors are logged in error.log while debugging messages are sent
to the console.
"""

import logging
import os
from dotenv import load_dotenv

load_dotenv()

JAUTOMATE_LOG_LEVEL = os.getenv('JAUTOMATE_LOG_LEVEL', 'INFO')
J_LOG_FILE = os.getenv('J_LOGS')
J_LOG_FILE_LEVEL = os.getenv('J_LOG_FILE_LEVEL', 'ERROR')


def init_logger():
    # Set up logging, debug will output to stream, errors will log to file.
    logger = logging.getLogger("Jautomate")
    logger.setLevel(JAUTOMATE_LOG_LEVEL)

    if J_LOG_FILE:
        logger_file = logging.FileHandler(J_LOG_FILE)
        logger_file.setLevel(J_LOG_FILE_LEVEL)
        error_formater = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger_file.setFormatter(error_formater)
        logger.addHandler(logger_file)

    logger_stream = logging.StreamHandler()
    logger_stream.setLevel(JAUTOMATE_LOG_LEVEL)
    debug_formater = logging.Formatter(
        '%(asctime)s - %(name)s - %(message)s',
        '%d-%m-%Y: %H:%M:%S'
    )
    logger_stream.setFormatter(debug_formater)

    logger.addHandler(logger_stream)

    return logger


j_logger = init_logger()
