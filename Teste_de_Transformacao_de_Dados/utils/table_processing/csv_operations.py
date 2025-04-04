#!/usr/bin/env python3
"""
CSV Operations Module

This module contains functions for exporting pandas DataFrames to CSV files
and handling CSV-related operations for PDF table extraction results.

Functions:
    save_tables_to_csv: Save multiple tables to CSV files
    table_to_csv: Convert a single table to CSV format with enhanced options
"""

import os
import pandas as pd
import logging
from typing import List

from pandas import DataFrame
import csv

from utils.ensure_directory_exists import ensure_directory_exists

logger = logging.getLogger(__name__)


def table_to_csv(
        df: pd.DataFrame,
        output_path: str,
        index: bool = False,
        encoding: str = 'utf-8',
) -> bool:
    """
    Convert a single pandas DataFrame to a CSV file with enhanced options.

    Args:
        df: DataFrame to export
        output_path: Path where the CSV file will be saved
        index: Whether to include DataFrame index in output
        encoding: Character encoding for the CSV file

    Returns:
        True if successful, False otherwise
    """
    if df is None or df.empty:
        logger.warning(f"Cannot save empty DataFrame to {output_path}")
        return False

    try:
        # Ensure directory exists
        ensure_directory_exists(os.path.dirname(os.path.abspath(output_path)))

        # Process text columns to handle newlines
        for col in df.columns:
            if df[col].dtype == object:  # Only process string columns
                # Replace newlines with spaces in text fields
                df[col] = df[col].apply(
                    lambda x: x.replace('\n', ' ').replace('\r', ' ') if isinstance(x, str) else x
                )

        # Save to CSV with proper quoting and NaN handling
        df.to_csv(
            output_path,
            index=index,
            encoding=encoding,
            na_rep='',  # Replace NaN with empty string
            quoting=csv.QUOTE_ALL,  # Quote all fields
            quotechar='"',  # Use double quotes
            doublequote=True,  # Properly escape quotes within fields
        )

        logger.info(f"Successfully saved table to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving table to {output_path}: {e}")
        return False


def save_tables_to_csv(
        tables: DataFrame,
        output_dir: str,
        base_filename: str,
        clean_headers: bool = True,
        encoding: str = 'utf-8'
) -> List[str]:
    """
    Save combined table to CSV file.

    Args:
        tables: DataFrame
        output_dir: Directory to save CSV files
        base_filename: Base name for CSV files
        clean_headers: Whether to clean table headers
        encoding: Character encoding for the CSV files

    Returns:
        List of paths to saved CSV files
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    saved_files = []

    # Create filename for combined table
    filename = f"{base_filename}_combined.csv"
    filepath = os.path.join(output_dir, filename)

    # Save to CSV
    if table_to_csv(tables, filepath,index=False, encoding=encoding):
        saved_files.append(filepath)

    if saved_files:
        logger.info(f"Saved {len(saved_files)} CSV files to {output_dir}")
    else:
        logger.warning("No CSV files were saved")

    return saved_files
