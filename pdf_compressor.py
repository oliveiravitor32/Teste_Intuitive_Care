#!/usr/bin/env python3
"""
File Compressor Module

This module provides functionality to compress files into ZIP archives.
It can be used as a standalone tool or imported into other Python scripts.

Usage:
    Import the module: from pdf_compressor import compress_files
    Or run directly: python pdf_compressor.py source_directory output_directory [output_filename]

Author: Vitor Oliveira
Date: 2025-03-25
"""


import os
import sys
import logging
import zipfile
from datetime import datetime
from typing import Optional

from utils.ensure_directory_exists import ensure_directory_exists


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def compress_files(source_dir: str, output_dir: str, output_filename: Optional[str] = None) -> bool:
    """
    Compress all files in the source directory into a ZIP archive in the output directory.

    Args:
        source_dir: Directory containing files to compress
        output_dir: Directory where the ZIP file will be saved
        output_filename: Name of the output ZIP file (default: auto-generated name)

    Returns:
        True if compression successful, False otherwise
    """


    try:
        # Normalize paths for cross-platform compatibility
        source_dir = os.path.normpath(source_dir)
        output_dir = os.path.normpath(output_dir)

        if not ensure_directory_exists(source_dir):
            logger.error(f"Source directory '{source_dir}' does not exist")
            return False

        if not ensure_directory_exists(output_dir):
            logger.error(f"Cannot create output directory '{output_dir}'")
            return False

        if not output_filename:
            # Generate filename with timestamp if none provided
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"anexos_{timestamp}.zip"

        # Ensure the output filename has .zip extension
        if not output_filename.endswith('.zip'):
            output_filename += '.zip'

        # Full path for the zip file
        zip_path = os.path.join(output_dir, output_filename)

        file_count = 0
        logger.info(f"Compressing files from {source_dir} to {zip_path}")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from the directory
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip (with path relative to source_dir)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    file_count += 1

        if file_count == 0:
            logger.warning(f"No files found in {source_dir} to compress")
            return False

        logger.info(f"Successfully compressed {file_count} files into {output_filename}")
        return True
    except Exception as e:
        logger.error(f"Failed to compress files: {e}")
        return False


if __name__ == "__main__":
    # When run directly, allow using from command line
    if len(sys.argv) < 3:
        print(f"Usage: python {os.path.basename(__file__)} source_directory output_directory [output_filename]")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    output_filename = sys.argv[3] if len(sys.argv) > 3 else None

    if compress_files(source_dir, output_dir, output_filename):
        print(f"Compression completed successfully.")
        sys.exit(0)
    else:
        print(f"Compression failed. See log for details.")
        sys.exit(1)