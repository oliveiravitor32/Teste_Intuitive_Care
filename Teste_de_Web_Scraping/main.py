#!/usr/bin/env python3
"""
ANS PDF Document Scraper

This application scrapes PDF annexes from the Brazilian National Health Agency (ANS) website
and compresses them into a ZIP archive. It serves as the main entry point for the PDF management
workflow, orchestrating the scraping and compression processes.

The application uses modular architecture with separate components for:
- PDF downloading (pdf_downloader module)
- File compression (pdf_compressor module)
- Shared utilities (utils package)

Usage:
    python main.py

Author: Vitor Oliveira
Date: 2025-03-25
"""

import os
import sys
import logging
from datetime import datetime

from pdf_scrapper import scrape_pdfs
from pdf_compressor import compress_files


# Default configuration
CONFIG = {
    "url": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos",
    "download_dir": "downloaded_files",
    "compress_dir": "compressed_files",
    "keywords": ["anexo"],
    "max_downloads": 2,
    "log_level": logging.INFO
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging with file and console handlers"""
    logging.basicConfig(
        level=CONFIG["log_level"],
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create log directory if needed
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Add file handler for persistent logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(f"logs/pdf_manager_{timestamp}.log")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    logging.getLogger().addHandler(file_handler)


def main() -> int:
    """
    Main function that orchestrates the PDF scraping and compression workflow.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Parse arguments and setup
        setup_logging()

        logger.info("Starting ANS PDF Document Manager")

        # Download PDFs
        logger.info("Starting PDF scraping process")
        download_count = scrape_pdfs(
            url=CONFIG["url"],
            download_dir=CONFIG["download_dir"],
            keywords=CONFIG["keywords"],
            max_downloads=CONFIG["max_downloads"]
        )

        if download_count == 0:
            logger.warning("No PDFs were scraped. Skipping compression.")
            return 0

        # Compress downloaded files
        logger.info("Starting compression process")
        success = compress_files(
            source_dir=CONFIG["download_dir"],
            output_dir=CONFIG["compress_dir"]
        )

        if success:
            logger.info("Document management process completed successfully")
            return 0
        else:
            logger.error("Compression process failed")
            return 1

    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        logger.exception(f"Unhandled error in main process: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
