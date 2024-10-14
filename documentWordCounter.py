import requests
from bs4 import BeautifulSoup
import re
from PyPDF2 import PdfReader
from io import BytesIO
from collections import defaultdict
from nltk.corpus import words

# Function to count words in a given text
def count_words(text, word_freq):
    words = re.findall(r'\w+', text.lower())  # Tokenize and convert to lowercase
    for word in words:
        word_freq[word] += 1

# Function: Retreive all links from webpage and contents of hyperlinks
def count_words_in_hyperlinks(url, visited_urls, word_freq):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all anchor tags with 'href' attribute
            links = soup.find_all('a', href=True)

            for link in links:
                linked_url = link['href']

                # Ensure that the linked URL is an absolute URL (including both http and https)
                if not linked_url.startswith(('http://', 'https://')):
                    linked_url = url + linked_url

                # Check if the linked URL has already been visited
                if linked_url not in visited_urls:
                    visited_urls.add(linked_url)  # Mark it as visited

                    try:
                        # Send an HTTP request to the linked URL
                        linked_response = requests.get(linked_url)
                        if linked_response.status_code == 200:
                            # Process the linked content here
                            if linked_url.lower().endswith(('.html', '.htm', '.txt')):
                                linked_soup = BeautifulSoup(linked_response.text, 'html.parser')
                                linked_page_text = linked_soup.get_text()
                                count_words(linked_page_text, word_freq)

                            elif linked_url.lower().endswith('.pdf'):
                                if 'syllabus.COMP78130.pdf' not in linked_url:
                                    linked_response = requests.get(linked_url, stream=True)
                                    if linked_response.status_code == 200:
                                        # Wrap the content in a BytesIO object
                                        pdf_content = BytesIO(linked_response.content)
                                        pdf = PdfReader(pdf_content)
                                        pdf_text = ''
                                        for page in pdf.pages:
                                            pdf_text += page.extract_text()
                                        count_words(pdf_text, word_freq)

                    except requests.exceptions.RequestException as ex:
                        # Handle exceptions as needed
                        pass

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# URL of the main webpage to analyze
webpage_url = 'https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/'

# Set which contains all links which have been processed
visited_urls = set()
word_freq = defaultdict(int)

# Calling the function to count words in hyperlinks page contents
count_words_in_hyperlinks(webpage_url, visited_urls, word_freq)

# URL of the specific webpage to analyze
specific_link = 'http://tartarus.org/~martin/PorterStemmer/'

try:
    # Send an HTTP GET request to the specific URL
    specific_response = requests.get(specific_link)
    if specific_response.status_code == 200:
        # Parse the HTML content
        specific_soup = BeautifulSoup(specific_response.text, 'html.parser')

        # Extract text content from the specific page and count words
        specific_page_text = specific_soup.get_text()
        count_words(specific_page_text, word_freq)

except requests.exceptions.RequestException as ex:
 # Handle exceptions for the special links like http://tartarus.org/~martin/PorterStemmer/
    print(f"Error processing {specific_link}: {str(ex)}")

# Print all words and their frequencies
print(word_freq)


