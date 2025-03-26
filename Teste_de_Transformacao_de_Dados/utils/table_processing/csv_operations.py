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
from typing import List, Optional, Union, Dict

from pandas import DataFrame

from .table_operations import combine_tables
from .data_cleaning import clean_table_headers

logger = logging.getLogger(__name__)


def table_to_csv(
        df: pd.DataFrame,
        output_path: str,
        index: bool = False,
        encoding: str = 'utf-8',
        clean_headers: bool = True
) -> bool:
    """
    Convert a single pandas DataFrame to a CSV file with enhanced options.

    Args:
        df: DataFrame to export
        output_path: Path where the CSV file will be saved
        index: Whether to include DataFrame index in output
        encoding: Character encoding for the CSV file
        clean_headers: Whether to clean column headers before export

    Returns:
        True if successful, False otherwise
    """
    if df is None or df.empty:
        logger.warning(f"Cannot save empty DataFrame to {output_path}")
        return False

    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Clean headers if requested
        if clean_headers:
            df = clean_table_headers(df)

        # Save to CSV
        df.to_csv(output_path, index=index, encoding=encoding)
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
    if table_to_csv(tables, filepath,
                    index=False, encoding=encoding,
                    clean_headers=clean_headers):
        saved_files.append(filepath)

    if saved_files:
        logger.info(f"Saved {len(saved_files)} CSV files to {output_dir}")
    else:
        logger.warning("No CSV files were saved")

    return saved_files
