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
