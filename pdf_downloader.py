"""
ANS PDF Downloader

This script downloads PDF annexes from the Brazilian National Health Agency (ANS) website.
It specifically targets PDF files containing the keyword 'anexo' in their link text,
downloads up to a configured maximum number of files, and saves them to a specified directory.

The tool includes logging, error handling, and validation to ensure reliable operation.

Usage:
    python pdf_downloader.py

Author: Vitor Oliveira
Date: 2025-03-26
"""


import os
import sys
import logging
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
DOWNLOAD_DIR = "assets"
KEYWORDS = ["anexo"]
MAX_DOWNLOADS = 2


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
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


def ensure_directory_exists(directory: str) -> bool:
    """
        Ensure the specified directory exists, creating it if necessary.

        Args:
            directory: Path to check/create

        Returns:
            True if directory exists or was created, False otherwise
    """

    try:
        if not os.path.exists(directory):
            logger.info(f"Creating directory: {directory}")
            os.makedirs(directory)
        return True
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def download_pdfs():
    """
      Main function to download PDF files from ANS website.

      Orchestrates the process of creating the download directory,
      fetching the page, extracting PDF links, and downloading files
      that match the specified criteria.
    """

    if not ensure_directory_exists(DOWNLOAD_DIR):
        logger.error("Cannot proceed without valid download directory")
        return

    # Fetch and parse the page
    parsed_data = fetch_and_parse_page_content(URL)
    if not parsed_data:
        logger.error("Cannot proceed without page content")
        return

    # Extract relevant PDF links
    pdf_links = extract_pdf_links(parsed_data, KEYWORDS)
    if not pdf_links:
        logger.warning("No matching PDFs found")
        return

    # Download PDFs (limited to MAX_DOWNLOADS)
    download_count = 0
    for i, pdf_url in enumerate(pdf_links[:MAX_DOWNLOADS]):
        # Ensure absolute URL
        if not pdf_url.startswith(("http://", "https://")):
            pdf_url = urljoin(URL, pdf_url)

        # Create a meaningful filename
        file_path = os.path.join(DOWNLOAD_DIR, f"Anexo_{i + 1}.pdf")

        # Download the PDF file
        if download_pdf(pdf_url, file_path):
            download_count += 1

    logger.info(f"Download process completed. Downloaded {download_count} PDFs.")


if __name__ == "__main__":
    try:
        download_pdfs()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)
