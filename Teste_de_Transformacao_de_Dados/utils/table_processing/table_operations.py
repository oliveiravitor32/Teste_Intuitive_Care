#!/usr/bin/env python3
"""
Table Operations Module

This module contains functions for manipulating and combining pandas DataFrames
extracted from tabular data in PDFs.

Functions:
    combine_tables: Merge multiple tables into a single table
"""

import pandas as pd
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


def combine_tables(tables_list: List[pd.DataFrame], keep_headers: bool = False) -> Optional[pd.DataFrame]:
    """
    Combine multiple pandas DataFrames into a single DataFrame vertically.

    This function handles tables that may have different column structures by
    aligning columns and handling missing or extra columns appropriately.

    Args:
        tables_list: List of pandas DataFrames to combine vertically
        keep_headers: How to handle headers in subsequent tables
            - If False (default): Headers from tables after the first are removed
              to prevent duplicate headers in the combined data
            - If True: All rows from all tables are kept, including potential header rows

    Returns:
        A single DataFrame containing all tables concatenated vertically,
        with consistent column structure. Returns None if tables_list is empty.

    Notes:
        - Tables with different column structures will be aligned to match the first table
        - Missing columns will be filled with None values
        - Extra columns not in the first table will be dropped
        - Column order is preserved based on the first table
    """
    if not tables_list:
        logger.warning("No tables to combine")
        return None

    if len(tables_list) == 1:
        logger.info("Only one table found, no need to combine")
        return tables_list[0]

    # Check that all tables have the same columns
    first_columns = set(tables_list[0].columns)
    for i, table in enumerate(tables_list[1:], 2):
        table_columns = set(table.columns)
        if table_columns != first_columns:
            logger.warning(f"Table {i} has different columns than the first table")
            # Try to align columns
            missing_cols = first_columns - table_columns
            extra_cols = table_columns - first_columns
            if missing_cols:
                for col in missing_cols:
                    table[col] = None
            if extra_cols:
                table = table.drop(columns=extra_cols)

    # Match column order to first table
    for i in range(1, len(tables_list)):
        tables_list[i] = tables_list[i][tables_list[0].columns]

    # Combine tables
    if keep_headers:
        combined = pd.concat(tables_list, ignore_index=True)
    else:
        # Remove header rows (which often get included as data rows) from subsequent tables
        combined = tables_list[0].copy()
        for table in tables_list[1:]:
            # Skip rows that match the header pattern
            header_pattern = combined.columns.tolist()
            mask = ~table.iloc[:, 0].astype(str).str.contains(header_pattern[0], regex=False)
            combined = pd.concat([combined, table[mask]], ignore_index=True)

    logger.info(f"Combined {len(tables_list)} tables into one with {len(combined)} rows")
    return combined
