
import os
import json

# Change the working directory to the directory containing preprocessed files
os.chdir(r"C:\Users\prath\Desktop\1k docs only\1kpreprocOnly")

# loading the list of all preprocessed files to a variable
listOfFiles = os.listdir()

def FileReader(file_name):
    with open(file_name, 'r',encoding='utf-8') as fn:
        textOfFile = fn.read()
    return textOfFile

def collectTerms(raw_File_Content):
    # Split the document string into separate words/tokens.
    split_terms = raw_File_Content.split()
    return split_terms

def setTF(terms):
    termFq = {}
    for term in terms:
        if term in termFq:
            termFq[term] += 1
        else:
            termFq[term] = 1
    return termFq

# Initialize the inverted index and document frequency empty dictionaries
invIndex = {}
docFq = {}

# Iterate through files in source directory 
for filename in listOfFiles:
    rawFileContent = FileReader(filename)
    terms = collectTerms(rawFileContent)

    # Calculate term frequency (tf) for this document
    termFq = setTF(terms)

    # Update the document frequency(df) for unique terms in this document
    for term in termFq:
        if term in docFq:
            docFq[term] += 1
        else:
            docFq[term] = 1

    # Update the inverted index
    for term, freq in termFq.items():
        if term not in invIndex:
            invIndex[term] = []
        invIndex[term].append((filename, freq))


os.chdir(r"C:\Users\prath\Desktop\1k docs only")

print(invIndex)
#storing the output(invertedindexfile) dictionary as a json file

#with open('1kinvind.json', 'w') as index_file:
 #   json.dump({"1kinvind": invIndex, "document_frequency": docFq}, index_file)

#print("The inverted index of documents and document frequency have been saved to 'newidf2.json'")