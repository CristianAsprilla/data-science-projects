"""
General utility functions for the churn prediction project.

This module provides common utility functions used across the project,
such as logging setup and other helper functions.
"""

import logging
from typing import Any


def setup_logger(name: str, log_file: str, level: Any = logging.INFO) -> logging.Logger:
    """
    Create and configure a logger with file output.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level: Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        Configured logger instance.
    """
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger