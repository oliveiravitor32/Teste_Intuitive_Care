"""
ANS PDF Scraper

This module scrapes and downloads PDF annexes from the Brazilian National Health Agency (ANS) website.
It specifically targets PDF files containing specified keywords in their link text,
downloads up to a configured maximum number of files, and saves them to a specified directory.

The module includes logging, error handling, and validation to ensure reliable operation.

Usage:
    from pdf_scraper import scrape_pdfs

    files_downloaded = scrape_pdfs(
        url="https://example.com",
        download_dir="downloads",
        keywords=["anexo"],
        max_downloads=2
    )

Author: Vitor Oliveira
Date: 2025-03-25
"""

import os
import logging
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils.ensure_directory_exists import ensure_directory_exists


# Configure logging
logger = logging.getLogger(__name__)


def fetch_and_parse_page_content(url: str) -> Optional[BeautifulSoup]:
    """
    Fetch and parse HTML content from a specified URL.

    Args:
        url: The URL to fetch content from

    Returns:
        BeautifulSoup object with parsed content or None if request fails
    """

    try:
        logger.info(f"Fetching page {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch page: {e}")
        return None


def extract_pdf_links(parsed_data: BeautifulSoup, keywords: List[str]) -> List[str]:
    """
    Extract PDF links containing specified keywords from parsed HTML.

    Args:
        parsed_data: BeautifulSoup object with parsed HTML
        keywords: List of keywords to match in link text

    Returns:
        List of URLs to PDF files matching criteria
    """

    pdf_download_links = []

    if not parsed_data:
        return pdf_download_links

    # Use CSS selector to pre-filter only links with PDF extensions
    pdf_links = parsed_data.select('a[href$=".pdf"]')

    for link in pdf_links:
        href = link.get('href')
        # Handle Empty or None link.string Values
        link_text = link.get_text().lower() if link.string else ""

        # Filter for files that contain the keywords
        if any(keyword in link_text for keyword in keywords):
                pdf_download_links.append(href)

    logger.info(f"Found {len(pdf_download_links)} matching PDF links")
    return pdf_download_links


def download_pdf(url: str, filename: str) -> bool:
    """
    Download a PDF file from a URL and save it locally.

    Args:
        url: The URL of the PDF to download
        filename: Local path where the PDF should be saved

    Returns:
        True if download successful, False otherwise
    """

    try:
        logger.info(f"Downloading {url} to {filename}")
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        logger.info(f"Successfully downloaded {filename}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download PDF: {e}")
        return False
    except IOError as e:
        logger.error(f"Failed to save PDF: {e}")
        return False


def scrape_pdfs(url: str,
    download_dir: str,
    keywords: List[str],
    max_downloads: int) -> bool:
    """
    Scrape and download PDF files from specified website that match given keywords.

    Args:
        url: URL to fetch PDF files from
        download_dir: Directory where files will be saved
        keywords: List of keywords to match in link text (default: ["anexo"])
        max_downloads: Maximum number of PDFs to download (default: 2)

    Returns:
        Number of successfully downloaded files
    """

    if not ensure_directory_exists(download_dir):
        logger.error("Cannot proceed without valid download directory")
        return

    # Fetch and parse the page
    parsed_data = fetch_and_parse_page_content(url)
    if not parsed_data:
        logger.error("Cannot proceed without page content")
        return

    # Extract relevant PDF links
    pdf_links = extract_pdf_links(parsed_data, keywords)
    if not pdf_links:
        logger.warning("No matching PDFs found")
        return

    # Download PDFs (limited to MAX_DOWNLOADS)
    download_count = 0
    for i, pdf_url in enumerate(pdf_links[:max_downloads]):
        # Ensure absolute URL
        if not pdf_url.startswith(("http://", "https://")):
            pdf_url = urljoin(url, pdf_url)

        # Create a meaningful filename
        file_path = os.path.join(download_dir, f"Anexo_{i + 1}.pdf")

        # Download the PDF file
        if download_pdf(pdf_url, file_path):
            download_count += 1

    logger.info(f"Scraping process completed. Downloaded {download_count} PDFs.")
