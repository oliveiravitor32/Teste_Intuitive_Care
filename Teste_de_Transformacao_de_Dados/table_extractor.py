#!/usr/bin/env python3
"""
PDF Table Extractor

This module extracts tables from PDF files using tabula-py and converts them
to structured pandas DataFrames which can then be exported to CSV.

Usage:
    from table_extractor import extract_tables_from_pdf

    tables = extract_tables_from_pdf("document.pdf")
    for i, table in enumerate(tables):
        table.to_csv(f"table_{i}.csv", index=False)

Dependencies:
    - tabula-py
    - pandas
    - Java Runtime Environment (JRE) for tabula-py

Author: Vitor Oliveira
Date: 2025-03-26
"""

import os
import logging
from typing import List, Optional, Dict, Any, Union
import pandas as pd
import tabula
import PyPDF2

# Configure logging
logger = logging.getLogger(__name__)


def get_pdf_metadata(filepath: str) -> Dict[str, Any]:
    """
    Extract metadata from a PDF file.

    Args:
        filepath: Path to the PDF file

    Returns:
        Dictionary containing PDF metadata
    """
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            info = reader.metadata

            # Create a normalized metadata dictionary
            metadata = {
                'page_count': len(reader.pages),
                'title': info.title if info.title else 'Unknown',
                'author': info.author if info.author else 'Unknown',
                'creator': info.creator if info.creator else 'Unknown',
                'producer': info.producer if info.producer else 'Unknown'
            }

        logger.info(f"Extracted metadata from {filepath}: {len(reader.pages)} pages")
        return metadata

    except Exception as e:
        logger.error(f"Failed to extract metadata: {e}")
        return {
            'page_count': 0,
            'title': 'Unknown',
            'author': 'Unknown',
            'creator': 'Unknown',
            'producer': 'Unknown'
        }


def extract_tables_from_pdf(
        filepath: str,
        pages: Union[str, List[int]] = 'all',
        area: Optional[List[float]] = None,
        guess: bool = True,
        lattice: bool = True,
        multiple_tables: bool = True
) -> List[pd.DataFrame]:
    """
    Extract tables from a PDF file using tabula-py.

    Args:
        filepath: Path to the PDF file
        pages: Page numbers to extract tables from ('all' or a list of page numbers)
        area: Coordinates [top, left, bottom, right] to extract tables from
        guess: Whether to guess table structure from non-bordered tables
        lattice: Whether to use lattice mode for bordered tables
        multiple_tables: Whether to extract multiple tables per page

    Returns:
        List of pandas DataFrames containing extracted tables
    """
    if not os.path.exists(filepath):
        logger.error(f"PDF file not found: {filepath}")
        return []

    try:
        logger.info(f"Extracting tables from {filepath} (pages: {pages})")

        # Get page count for validation
        metadata = get_pdf_metadata(filepath)
        page_count = metadata['page_count']

        if page_count == 0:
            logger.error(f"Invalid or empty PDF: {filepath}")
            return []

        # Extract tables using tabula
        tables = tabula.read_pdf(
            filepath,
            pages=pages,
            area=area,
            guess=guess,
            lattice=lattice,
            multiple_tables=multiple_tables
        )

        logger.info(f"Extracted {len(tables)} tables from {filepath}")

        # Filter out empty tables
        non_empty_tables = [table for table in tables if not table.empty]

        if len(non_empty_tables) < len(tables):
            logger.warning(f"Filtered out {len(tables) - len(non_empty_tables)} empty tables")

        return non_empty_tables

    except Exception as e:
        logger.exception(f"Error extracting tables: {e}")
        return []


def clean_table_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean up table headers, replacing None or numeric values with reasonable column names.

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


def save_tables_to_csv(
        tables: List[pd.DataFrame],
        output_dir: str,
        base_filename: str,
        clean_headers: bool = True
) -> List[str]:
    """
    Save extracted tables to CSV files.

    Args:
        tables: List of pandas DataFrames
        output_dir: Directory to save CSV files
        base_filename: Base name for CSV files
        clean_headers: Whether to clean table headers

    Returns:
        List of paths to saved CSV files
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    saved_files = []

    for i, table in enumerate(tables):
        if table.empty:
            continue

        if clean_headers:
            table = clean_table_headers(table)

        # Create filename with index
        filename = f"{base_filename}_table_{i + 1}.csv"
        filepath = os.path.join(output_dir, filename)

        # Save to CSV
        try:
            table.to_csv(filepath, index=False)
            saved_files.append(filepath)
            logger.info(f"Saved table to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save table to {filepath}: {e}")

    return saved_files


if __name__ == "__main__":
    # Configure logging when run directly
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python table_extractor.py <pdf_file> [output_directory]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    tables = extract_tables_from_pdf(pdf_file)
    if tables:
        base_filename = os.path.splitext(os.path.basename(pdf_file))[0]
        saved_files = save_tables_to_csv(tables, output_dir, base_filename)
        print(f"Saved {len(saved_files)} tables to {output_dir}")
    else:
        print("No tables found in the PDF")