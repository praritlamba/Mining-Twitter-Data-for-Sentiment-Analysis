# Mining-Twitter-Data-for-Sentiment-Analysis
Sentiment Analysis using tweepy,NLTK and Textblob

Using OAuth to make connection twitter
```
import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

```

Collecting tweets in json file
```
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
```


The key attributes of the tweets pulled out are :
* text: the text of the tweet itself
*	created_at: the date of creation
*	favorite_count, retweet_count: the number of favourites and retweets
*	favorited, retweeted: boolean stating whether the authenticated user (you) have favourited or retweeted this tweet
*	lang: acronym for the language (e.g. “en” for english)
*	id: the tweet identifier
*	place, coordinates, geo: geo-location information if available
*	user: the author’s full profile
*	entities: list of entities like URLs, @-mentions, hashtags and symbols
*	in_reply_to_user_id: user identifier if the tweet is a reply to a specific user
*	in_reply_to_status_id: status identifier id the tweet is a reply to a specific status


1. Processing tweets
  1. Tokenizing the tweet
  2. Tokenizing @-mentions, emoticons, URLs and #hash-tags  as individual tokens.

```
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
```

The regular expressions are compiled with the flags re.VERBOSE, to allow spaces in the regexp to be ignored (see the multi-line emoticons regexp), and re.IGNORECASE to catch both upper and lowercases. Thetokenize() function simply catches all the tokens in a string and returns them as a list. 
```
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
```

Removing stop-words,punctuations and rt,via words :
```
from nltk.corpus import stopwords
import string

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
```

In order to keep track of the frequencies while we are processing the tweets, we can use collections.Counter() which internally is a dictionary (term: count) with some useful methods like most_common():
```
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
        # Update the counter
	    #terms_single = set(terms_all)
		# Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text']) 
              if term.startswith('#')]
# Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text']) 
              if term not in stop and
              not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs
```

####Python TextBlob Sentiment Analysis

Sentiment Analysis refers to the process of taking natural language to identify and extract subjective information. You can take text, run it through the TextBlob and the program will spit out if the text is positive, neutral, or negative by analyzing the language used in the text.

|Sentiment Analysis            |                                         |
|----------------------------- | -----------------------------------------|
|Text | If that is not cool enough for you than that is a you problem. |
|Polarity | -0.0875 |
|Subjectivity | 0.575 |
|Classification | neg |
|P_Pos | 0.344455873 |
|P_Neg | 0.655544127 |


What does that mean?
* Polarity - a measure of the negativity, the neutralness, or the positivity of the text
* Classification - either pos or neg indicating if the text is positive or negative


To calculate the overall sentiment, we look at the polarity score:
* Positive – from .01 to 1
* Neutral – 0
* Negative – from –.01 to -1

```
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
```

