import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import fitz
import json
from concurrent.futures import ThreadPoolExecutor

# Create a dictionary to store filename-link pairs
IndexData = {}

def UpdateIndexFile(indexFilePath, data):
    """
    Update the index file with the provided data.

    :param indexFilePath: Path to the index file.
    :param data: Data to be written to the index file.
    """
    with open(indexFilePath, 'w') as index_file:
        json.dump(data, index_file)

# Specify the path for the index file in the same directory
outDirectory = r'C:\Users\prath\OneDrive\Documents\Information Retreival\IR_Assignment06\TenKdocuments'
os.makedirs(outDirectory, exist_ok=True)
indexFilePath = os.path.join(outDirectory, 'index_file.json')

def UrlExtractor(url):
    """
    Retrieve and parse links from a given URL.

    :param url: URL to retrieve links from.
    :return: List of links found on the page.
    """
    links = []

    try:
        response = requests.get(url, timeout=10)  # Adjust the timeout value as needed
        if response.status_code == 200:
            page_content = response.text

            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')

            # Find and extract all links from the page
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                links.append(absolute_url)

    except Exception as e:
        print(f"Error retrieving links from {url}: {e}")

    return links

def ExtractTextAsString(url):
    """
    Extract text content from a given URL.

    :param url: URL to extract text from.
    :return: Extracted text content.
    """
    try:
        response = requests.get(url, timeout=10)  # Adjust the timeout value as needed

        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')

            if 'pdf' in content_type or '.pdf' in url:
                try:
                    pdfFile = open('temp.pdf', 'wb')
                    pdfFile.write(response.content)
                    pdfFile.close()

                    pdfText = ''
                    with fitz.open('temp.pdf') as pdf_document:
                        for page_number in range(pdf_document.page_count):
                            page = pdf_document.load_page(page_number)
                            pdfText += page.get_text()

                    return pdfText
                except Exception as e:
                    print(f"Error reading PDF from URL: {url}\n{e}")
                    return None

            elif 'html' in content_type:
                soup = BeautifulSoup(response.text, 'html.parser')
                htmlText = soup.get_text()
                return htmlText

            elif 'php' in content_type or '.txt' in url:
                return response.text

    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {e}")

    return None

def SavingFilesAndMetadata(text, directory, filename, source_url):
    """
    Count words in the text and save it to a file with metadata.

    :param text: Text content to be saved.
    :param directory: Directory to save the file in.
    :param filename: Name of the file.
    :param source_url: Source URL of the text content.
    :return: True if the text is saved, False otherwise.
    """
    word_count = len(text.split())
    if word_count > 50:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"### METADATA:\n source URL: {source_url}\n Tokens on this document= {word_count}###")
            file.write(text)
        print(f"Word count ({word_count}) is greater than 50. String saved to {file_path} with metadata.")
        return True
    else:
        print(f"Word count ({word_count}) is not greater than 50. String not saved.")
        return False

# Replace the following URL with the starting URL you want to crawl from
start_url = "https://www.memphis.edu/"

successfully_saved_count = 0
visited_urls = set()
queue = [start_url]
delay_seconds = 0.05  # Reduce the delay (be cautious not to overload the server)

with ThreadPoolExecutor(max_workers=8) as executor:  # Set max_workers to 8 for faster crawling
    while successfully_saved_count < 10000 and queue:
        current_url = queue.pop(0)

        def process_url(url):
            global successfully_saved_count  # Make successfully_saved_count global
            try:
                if url not in visited_urls:
                    visited_urls.add(url)

                    links_on_page = UrlExtractor(url)
                    for link in links_on_page:
                        if link not in visited_urls and "memphis.edu" in url:
                            queue.append(link)

                    text = ExtractTextAsString(url)
                    if text is not None:
                        filename = f'doc_{successfully_saved_count}.txt'
                        if SavingFilesAndMetadata(text, outDirectory, filename, url):
                            # Update the index data with filename-link pair
                            IndexData[filename] = url
                            UpdateIndexFile(indexFilePath, IndexData)
                            successfully_saved_count += 1

            except requests.exceptions.RequestException as e:
                print(f"Request to {url} failed: {e}")

        # Concurrently process URLs
        futures = [executor.submit(process_url, current_url) for _ in range(8)]  # Use 8 workers

        # Wait for all futures to complete
        for future in futures:
            future.result()

        # Add a reduced delay before the next request
        time.sleep(delay_seconds)

# Save the final index data to the index file
UpdateIndexFile(indexFilePath, IndexData)
