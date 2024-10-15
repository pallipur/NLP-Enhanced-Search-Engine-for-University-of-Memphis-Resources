Project Overview:

The NLP Enhanced Search Engine for the University of Memphis is a web-crawling application designed to facilitate efficient information retrieval from the University of Memphis website. This project employs natural language processing (NLP) techniques to extract, index, and manage content from various web pages, enabling improved search capabilities.

web_scraper.py

This web scraper collects textual data from specified web pages. It extracts and saves content from the pages, enabling the system to build a corpus of documents for indexing. The crawler ensures that the collected data is diverse and representative of the target domain.

documentWordCounter.py:
This script counts the number of words in each document. It provides insights into the size of each document, which can be useful for analyzing text data and understanding document lengths in the context of information retrieval.

text_preprocessor.py
This script handles preprocessing of text data. It includes functions for tokenization, stemming, and stopword removal, preparing the text for indexing. Effective preprocessing is crucial for improving the quality and relevance of search results.

Inverted_Index_builder.py
This script is responsible for creating an inverted index from the collected documents. The inverted index maps keywords to their corresponding document identifiers, enabling efficient retrieval of documents based on search queries. This foundational component supports quick lookups for keyword searches.

doc_to_pdoc_converter.py
This utility converts standard document formats (e.g., text files) into processed documents (pdocs) that are optimized for indexing and searching. This transformation may involve text normalization, tokenization, and removal of stopwords, ensuring that the data is in the best format for indexing.

search_engine.py
This script implements the core functionality of the search engine. It handles user queries, retrieves relevant documents from the inverted index, and processes the search results to return to the user. This is the backend logic for executing searches.

search_engine_with_FlaskUI.py
This version of the search engine incorporates a Flask web framework to provide a web-based user interface. It allows users to interact with the search engine through a browser, submitting queries and receiving results dynamically.

index.html
This is the main HTML file that serves as the user interface for the search engine. It contains the layout and structure for presenting search results to users, allowing for interaction with the search functionality.

results.html
This HTML file is used to display the results of a search query. It formats the output of the search engine, presenting the relevant documents and their details in a user-friendly manner.
