import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import string
import json

def stopwords_from_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        words = word_tokenize(text)
        return words
    except requests.exceptions.RequestException as e:
        print(f"Error collecting words from {url}: {e}")
        return []
    
    
    
webpage_url = 'https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt'
stopwords = stopwords_from_webpage(webpage_url)
Query = "try throughout unfortunately america magic world data memphis gives probability couch hand of god give holy saint murder killer travelling mustard attitude psychopath irritate annoyance"


def preprocesser(Query, stopwords):
    digits_pattern = r'\d'
    no_digits = re.sub(digits_pattern, '', Query)
    
    punctuation_pattern = f"[{re.escape(string.punctuation)}]"
    no_punctuation = re.sub(punctuation_pattern, '', no_digits)
    
    lowercase_op = no_punctuation.lower()

    input_string = lowercase_op
    words = input_string.split()
    
    unstoppable_words = [word for word in words if word.lower() not in stopwords]
    
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in unstoppable_words]
    stemmed_text = [word for word in stemmed_text if "http" not in word and ".pdf" not in word and ".txt" not in word]

    stemmed_string = ' '.join(stemmed_text)
    return stemmed_string

newQuery = preprocesser(Query, stopwords)
print(newQuery)


def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def check_keywords_in_dictionary(keywords, dictionary):
    for keyword in keywords:
        if keyword in dictionary:
            print(f"Keyword '{keyword}' is present in the dictionary.")
            # You can perform additional actions here if needed
        else:
            print(f"Keyword '{keyword}' is not present in the dictionary.")
            
            
            

# Replace 'your_inverted_index_file.json' with the actual file path
inverted_index_file_path = r"C:\Users\prath\OneDrive\Documents\Information Retreival\IR_Assignment07\bigidf.json"

inverted_index = load_json(inverted_index_file_path)

list_keys=list(inverted_index.items())
print(list_keys)

#check_keywords_in_inverted_index(newQuery, inverted_index)