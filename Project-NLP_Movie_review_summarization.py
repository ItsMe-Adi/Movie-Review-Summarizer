#Summarization of Movie Reviews taken from Times Of India website.

import nltk
from requests import get
from bs4 import BeautifulSoup
import heapq

#Fetching text from web

weburl='https://timesofindia.indiatimes.com/entertainment/english/movie-reviews/pirates-of-the-caribbean-salazars-revenge/movie-review/58841177.cms'
htmlstring = get(weburl).text
html = BeautifulSoup(htmlstring, 'lxml')
entries = html.find_all('div', {'class':'Normal'})
text = [e.get_text() for e in entries]

#Converting Fetched text into string

string=""
for x in text:
    for y in x:
        string=string+y

#Tokenization

tokens=nltk.word_tokenize(string)

#Extracting the review part from string

f=0
review=[]
for x in tokens:
    if(x=='Review'):
        f=1;
    if(f==1):
        review.append(x)
        
#Converting review to a string
        
review_string=""
for i in review:
    review_string=review_string+" "+i

#Sentence,word Tokenization
    
sentence_token=nltk.sent_tokenize(review_string)
words_token=nltk.word_tokenize(review_string)

#Calculating word frequency

stopwords=nltk.corpus.stopwords.words('english')
word_freq={}

for word in words_token:
    if word not in stopwords:
        if word not in word_freq.keys():
            word_freq[word]=1
        else:
            word_freq[word]+=1
            
#Calculate weighted frequency
        
maximum_freq_word=max(word_freq.values())

for word in word_freq.keys():
    word_freq[word]=(word_freq[word]/maximum_freq_word)
    
#Calculate sentence score with each word weighted frequency
    
sentence_scores={}

for sentence in sentence_token:
    for word in nltk.word_tokenize(sentence):
        if(word in word_freq.keys()):
            if(len(sentence.split(' ')))<60:  #Only considering sentences with length less than 40
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence]=word_freq[word]
                else:
                    sentence_scores[sentence]+=word_freq[word]
                    
#Summarizing on the basis of top (n/2) sentence scores
#where n is the total number of sentences in sentence scores
                   
summary=heapq.nlargest(6, sentence_scores,key=sentence_scores.get)
print("Movie review summary:\n",summary)
                
#Analysis

summ_string=""
for a in summary:
    for b in a:
        summ_string=summ_string+b
        
print()
print('Total characters in summary',len(summ_string))
print()
print('Total characters in original review',len(review_string))
print()
print('Reduction in percentage',100-((len(summ_string)/len(review_string))*100),"%")










                
















        
        














