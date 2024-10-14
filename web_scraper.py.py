
import requests
from bs4 import BeautifulSoup
from nltk.corpus import words
import string


#user input url to fetch website content as a tree
url_input=input("Paste the url of which you want to count the words:")
r = requests.get(url_input)
HTMLcontent=r.content
#parsing tree into pieces
RawContent=BeautifulSoup(HTMLcontent,'html.parser')


TextContent=RawContent.get_text()

#preprocessing text : 
                #1.removing punctuation marks
                #2.splitting at whitespaces
                #3.Converting all words to lower case for proper sorting
OnlyText=TextContent.translate(str.maketrans('','',string.punctuation))
OnlyText=OnlyText.lower()
list_workspace=(OnlyText.split())
countofwords=(len(OnlyText.split()))
print("\nTotal words on the webpage:",countofwords)
list_workspace.sort()
print("\nplease wait while I filter the english words and sort them in alphabetical order....\n")



Ready_list=[]

#for loop for filtering out words found in oxford english dictionary
for item in list_workspace:
    if item in words.words():
        Ready_list.append(item)


Result={}


#for loop to calculate word frequencies.
for item in Ready_list:
   if item in Result:
      Result[item] += 1
   else:
      Result[item] = 1


#output of number of unique words and their frequencies
print("\nTotal meaningful english words:",len(Ready_list))
print("\n\n",Result)
        
        
        
        