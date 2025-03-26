"""
Directory Utilities Module

This module provides utility functions for directory operations,
particularly focused on directory validation and creation.

The primary function is `ensure_directory_exists`, which checks
if a directory exists and creates it if necessary, with proper
error handling and logging.

Usage:
    from utils.ensure_directory_exists import ensure_directory_exists

    if ensure_directory_exists('/path/to/directory'):
        # proceed with operations requiring the directory
    else:
        # handle directory creation failure

Author: Vitor Oliveira
Date: 2025-03-25
"""


import os
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def ensure_directory_exists(directory: str) -> bool:
    """
        Ensure the specified directory exists, creating it if necessary.

        Args:
            directory: Path to check/create

        Returns:
            True if directory exists or was created, False otherwise
    """

    try:
        if not os.path.exists(directory):
            logger.info(f"Creating directory: {directory}")
            os.makedirs(directory)
        return True
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False