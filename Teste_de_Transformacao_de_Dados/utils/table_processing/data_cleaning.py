#!/usr/bin/env python3
"""
Data Cleaning Module

This module contains functions for cleaning and standardizing data extracted
from PDF tables to ensure consistency and usability.

Functions:
    clean_table_headers: Standardize column names in a DataFrame
    standardize_data_types: Convert columns to appropriate data types
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def clean_table_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean up table headers by replacing missing, numeric, or malformed values
    with more appropriate column names.

    Args:
        df: pandas DataFrame with raw headers

    Returns:
        DataFrame with cleaned headers
    """
    if df.empty:
        return df

    # Create a copy to avoid modifying the original
    cleaned_df = df.copy()

    # Get current column names
    columns = cleaned_df.columns.tolist()

    # Replace None, NaN or numeric-only headers
    new_columns = []
    for i, col in enumerate(columns):
        # If column is None or NaN
        if pd.isna(col):
            new_col = f"Column_{i + 1}"
        # If column is a number
        elif str(col).replace('.', '', 1).isdigit():
            new_col = f"Column_{col}"
        # If column is empty string
        elif str(col).strip() == '':
            new_col = f"Column_{i + 1}"
        else:
            # Remove newlines and excessive spaces
            new_col = str(col).replace('\n', ' ').strip()
            while '  ' in new_col:
                new_col = new_col.replace('  ', ' ')

        new_columns.append(new_col)

    # Set new column names
    cleaned_df.columns = new_columns
    return cleaned_df


def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Attempt to convert DataFrame columns to appropriate data types based on content.

    This helps with sorting, filtering, and analysis of the extracted data.

    Args:
        df: DataFrame with raw column types

    Returns:
        DataFrame with standardized column types
    """
    if df.empty:
        return df

    # Create a copy to avoid modifying the original
    result_df = df.copy()

    # Try to convert numeric columns
    for col in result_df.columns:
        # Skip columns that are already numeric
        if pd.api.types.is_numeric_dtype(result_df[col]):
            continue

        # Try to convert to numeric
        try:
            numeric_series = pd.to_numeric(result_df[col], errors='coerce')
            # Only apply if most values were successfully converted (>50%)
            if numeric_series.notna().sum() / len(numeric_series) > 0.5:
                result_df[col] = numeric_series
        except Exception:
            pass

    # Try to convert date columns
    date_patterns = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']

    for col in result_df.columns:
        # Skip numeric columns
        if pd.api.types.is_numeric_dtype(result_df[col]):
            continue

        # Look for date-like patterns
        if result_df[col].astype(str).str.contains(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}').any():
            for pattern in date_patterns:
                try:
                    date_col = pd.to_datetime(result_df[col], format=pattern, errors='coerce')
                    if date_col.notna().sum() / len(date_col) > 0.5:
                        result_df[col] = date_col
                        break
                except Exception:
                    continue

    logger.info(f"Standardized data types for {len(result_df.columns)} columns")
    return result_df