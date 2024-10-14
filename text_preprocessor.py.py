import re
import os
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Constants for file paths
INPUT_DIRECTORY_PATH = r"C:\Users\prath\Desktop\Assignment 7 new\preprocess\inputpreprocess"
OUTPUT_DIRECTORY_PATH = r"C:\Users\prath\Desktop\Assignment 7 new\preprocess\outputpreprocess"
STOPWORDS_FILENAME = "stopwords.txt"

def preprocesser(file_name):
    try:
        # Read the file content
        with open(file_name, 'r', encoding='utf-8') as myfile:
            file_content = myfile.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return ""  # Return an empty string if the file is not found
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string in case of any other exception

    # Removing digits
    digits_pattern = r'\d'
    no_digits = re.sub(digits_pattern, '', file_content)
    
    # Removing punctuation
    punctuation_pattern = f"[{re.escape(string.punctuation)}]"
    no_punctuation = re.sub(punctuation_pattern, '', no_digits)
    
    # Convert the string to lowercase
    lowercase_op = no_punctuation.lower()
    
    # Load stopwords as a list from a file
    try:
        with open(STOPWORDS_FILENAME, 'r', encoding='utf-8') as stopwordsfile:
            raw_stopwords = stopwordsfile.read()
            to_stop = word_tokenize(raw_stopwords)
    except FileNotFoundError:
        print(f"Stopwords file '{STOPWORDS_FILENAME}' not found.")
        to_stop = []

    input_string = lowercase_op
    words = input_string.split()
    unstoppable_words = [word for word in words if word.lower() not in to_stop]
    
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in unstoppable_words]
    
    # Remove words containing "http", ".pdf", or ".txt"
    stemmed_text = [word for word in stemmed_text if "http" not in word and ".pdf" not in word and ".txt" not in word]

    stemmed_string = ' '.join(stemmed_text)

    return stemmed_string

def save_output(output_string, key_id):
    file_name = f"preProcDocument{key_id}.txt"
    file_path = os.path.join(OUTPUT_DIRECTORY_PATH, file_name)
   
    try:
        with open(file_path, "w", encoding='utf-8') as file:
            # Write the string to the file
            file.write(output_string)
    except Exception as e:
        print(f"An error occurred while writing to the output file: {e}")

# Initialize a counter variable to use it to incrementally name output files
key_id_counter = 0

# For loop to input text files to preprocessor
for file in os.listdir(INPUT_DIRECTORY_PATH):
    if file.endswith(".txt"):
        print(file)
        cleaned_text = preprocesser(os.path.join(INPUT_DIRECTORY_PATH, file))

        if cleaned_text:  # Check if cleaned_text is not an empty string
            print("Text pre processing done for",file)
            key_id_counter += 1  # Increment the counter
            save_output(cleaned_text, key_id_counter)
            
print("\n\nText of input files from 'TestFilesAssignment4' are pre-processed and loaded into 'post process directory'")