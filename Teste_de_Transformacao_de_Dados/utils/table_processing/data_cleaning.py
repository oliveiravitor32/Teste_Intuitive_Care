#!/usr/bin/env python3
"""
Data Cleaning Module

This module contains functions for cleaning and standardizing data extracted
from PDF tables to ensure consistency and usability.

Functions:
    standardize_data_types: Convert columns to appropriate data types
    expand_abbreviations: Expand abbreviations in column names and in cell values to their full form.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


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
    date_patterns = ['%d/%m/%Y']

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


def expand_abbreviations(df: pd.DataFrame, abbreviation_map: dict = None, expand_cell_values: bool = True) -> pd.DataFrame:
    """
    Expand abbreviations in column names and in cell values to their full form.

    Args:
        df: pandas DataFrame with columns or values containing abbreviations
        abbreviation_map: Dictionary mapping abbreviations to their expanded forms
            If None, default healthcare abbreviations will be used

    Returns:
        DataFrame with expanded abbreviations
    """
    if df is None or df.empty:
        return df

    # Create a copy to avoid modifying the original
    result_df = df.copy()

    # Default abbreviation mapping if none provided
    if abbreviation_map is None:
        abbreviation_map = {
            'OD': 'ODONTOLÓGICA',
            'AMB': 'AMBULATORIAL',
            #'HCO': 'HOSPITALAR COM OBSTETRÍCIA',
            #'HSO': 'HOSPITALAR SEM OBSTETRÍCIA',
            #'REF': 'REFERÊNCIA',
            #'PAC': 'PRECEDIMENTO DE ALTA COMPLEXIDADE',
            #'DUT': 'DIRETRIZ DE UTILIZAÇÃO'
        }

    # Rename columns that exactly match abbreviations
    columns_to_rename = {}
    for col in result_df.columns:
        if col in abbreviation_map:
            columns_to_rename[col] = abbreviation_map[col]

    if columns_to_rename:
        result_df = result_df.rename(columns=columns_to_rename)
        logger.info(f"Expanded {len(columns_to_rename)} column abbreviations")

    # Replace abbreviations in cell values if requested
    if expand_cell_values:
        logger.info("Expanding abbreviations in cell values")
        for col in result_df.columns:
            if result_df[col].dtype == object:  # Only process text columns
                # Create a mask for non-NaN values
                non_nan_mask = result_df[col].notna()

                # Only process non-NaN values
                if non_nan_mask.any():  # Only proceed if there are non-NaN values
                    for abbr, expanded in abbreviation_map.items():
                        # Apply replacement only to non-NaN values
                        result_df.loc[non_nan_mask, col] = result_df.loc[non_nan_mask, col].astype(str).str.replace(
                            r'\b' + abbr + r'\b',
                            expanded,
                            regex=True
                        )

    return result_df
