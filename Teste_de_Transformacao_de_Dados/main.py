#!/usr/bin/env python3
"""
PDF Table Extraction Tool

This tool extracts tables from PDF files and converts them to structured CSV files.
It supports various extraction strategies for different types of tables.

Usage:
    python main.py

Author: Vitor Oliveira
Date: 2025-03-26
"""

import os
import sys
import logging
import pandas as pd
from datetime import datetime

# Try to set up JVM first if the module exists
try:
    from utils.jvm_setup import setup_jvm
    setup_jvm()
except ImportError:
    print("JVM setup module not found. Continuing without explicit JVM configuration.")

# Import main extraction functions
from table_extractor import (
    extract_tables_from_pdf,
    get_pdf_metadata
)

from utils.table_processing import save_tables_to_csv
from utils.table_processing import combine_tables
from utils.table_processing import clean_table_headers, standardize_data_types, expand_abbreviations

# Configuration constants
INPUT_PDF = "Anexo_1.pdf"  # Replace with your PDF file path
OUTPUT_DIR = "output"
START_PAGE = 3  # Start from page 3
END_PAGE = None  # None means process until the end of the document
EXTRACTION_METHOD = "both"  # Options: "lattice", "stream", "both"
VERBOSE_LOGGING = True  # Set to True for more detailed logs


def setup_logging(log_level: int = logging.INFO) -> None:
    """
    Configure logging with file and console handlers.

    Args:
        log_level: Logging level to use
    """
    # Make sure logging is reset
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure logging with specified level
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler()  # Explicitly add console handler
        ]
    )

    # Create log directory if needed
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Add file handler with timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/table_extractor_{timestamp}.log"

    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))
        logging.root.addHandler(file_handler)
        print(f"Log file created: {log_file}")
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")


def main() -> int:
    """
    Main function that orchestrates the PDF table extraction workflow.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Setup logging
        log_level = logging.DEBUG if VERBOSE_LOGGING else logging.INFO
        setup_logging(log_level)
        logger = logging.getLogger(__name__)

        logger.info("Starting PDF Table Extraction Tool")

        # Validate input file
        if not os.path.exists(INPUT_PDF):
            logger.error(f"Input file does not exist: {INPUT_PDF}")
            return 1

        # Get PDF metadata to determine total pages
        metadata = get_pdf_metadata(INPUT_PDF)
        total_pages = metadata['page_count']
        logger.info(f"PDF has {total_pages} pages")

        # Determine page range (from START_PAGE to end of document)
        end_page = END_PAGE if END_PAGE is not None else total_pages

        # Create page range string for tabula-py
        # Tabula uses 1-based page numbering
        page_range = f"{START_PAGE}-{end_page}"
        logger.info(f"Processing pages {page_range}")

        # Extract tables
        extraction_params = {
            'lattice': EXTRACTION_METHOD in ['lattice', 'both'],
            'guess': EXTRACTION_METHOD in ['stream', 'both'],
            'pages': page_range
        }

        logger.info(f"Extracting tables using {EXTRACTION_METHOD} method")
        tables = extract_tables_from_pdf(
            INPUT_PDF,
            **extraction_params
        )

        if not tables:
            logger.warning("No tables found in the PDF")
            return 0

        logger.info(f"Found {len(tables)} tables in the document")

        # Example: Display info about the first table
        if tables and len(tables) > 0:
            first_table = tables[0]
            logger.info(f"First table has {len(first_table)} rows and {len(first_table.columns)} columns")
            logger.info(f"Columns: {', '.join(str(c) for c in first_table.columns)}")

        # Process tables - standardize data types and expand abbreviations in column names and cells
        processed_tables = []
        for i, table in enumerate(tables):
            # Clean headers
            clean_table = clean_table_headers(table)

            # Expand abbreviations in column names and cells only if requested
            expanded_table = expand_abbreviations(df = clean_table, expand_cell_values= True)

            # Standardize data types
            standard_table = standardize_data_types(expanded_table)

            processed_tables.append(standard_table)
            logger.info(f"Processed table {i + 1}: {len(table)} rows")

        # Create base filename from input file
        base_filename = os.path.splitext(os.path.basename(INPUT_PDF))[0]

        combined_tables = combine_tables(processed_tables)

        if combined_tables is None:
            logger.warning("The tables were not combined")
            return 0

        # Save tables to CSV
        saved_file = save_tables_to_csv(
            combined_tables,
            OUTPUT_DIR,
            base_filename,
            encoding='utf-8',
            clean_headers=True  # Already cleaned above, but param is required
        )

        if not saved_file:
            logger.warning("No tables were saved")
            return 0

        logger.info(f"Successfully saved {len(saved_file)} tables to {OUTPUT_DIR}")
        for file in saved_file:
            logger.info(f"  - {os.path.basename(file)}")

            # Show stats about the combined result
            combined_path = saved_file[0]
            combined_df = pd.read_csv(combined_path)
            logger.info(f"Combined table has {len(combined_df)} rows and {len(combined_df.columns)} columns")

        return 0

    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
        return 130
    except Exception as e:
        logging.exception(f"Unhandled error in main process: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
