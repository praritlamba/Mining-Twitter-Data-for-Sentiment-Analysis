import json
import re
import operator 
from textblob import TextBlob
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os, sys, codecs
from nltk import bigrams
reload(sys)
sys.setdefaultencoding('utf-8')
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via'] 
fname = 'python.json'
with open(fname, 'r') as f:
    lis=[]
    neg=0.0
    n=0.0
    net=0.0
    pos=0.0
    p=0.0
    count_all = Counter()
    cout=0
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        blob = TextBlob(tweet["text"])
        cout+=1
        lis.append(blob.sentiment.polarity)
        #print blob.sentiment.subjectivity
        #print (os.listdir(tweet["text"]))
        if blob.sentiment.polarity < 0:
            sentiment = "negative"
            neg+=blob.sentiment.polarity
            n+=1
        elif blob.sentiment.polarity == 0:
            sentiment = "neutral"
            net+=1
        else:
            sentiment = "positive"
            pos+=blob.sentiment.polarity
            p+=1

        # output sentiment
        
    print "Total tweets",len(lis)
    print "Positive ",float(p/cout)*100,"%"
    print "Negative ",float(n/cout)*100,"%"
    print "Neutral ",float(net/len(lis))*100,"%"
    #print lis
        # determine if sentiment is positive, negative, or neutral
        
        # output sentiment
        #print sentiment