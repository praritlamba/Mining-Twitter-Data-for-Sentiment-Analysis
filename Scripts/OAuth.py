from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
 
 
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
 



 
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
        
 
if __name__ == '__main__': 
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    twitter_stream = Stream(auth, MyListener())
    print("Writing Tweets")
    twitter_stream.filter(track=['bollywood'])
    #print("Writing Tweets")