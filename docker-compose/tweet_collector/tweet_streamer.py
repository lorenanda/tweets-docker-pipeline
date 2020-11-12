from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
from sqlalchemy import create_engine
import pymongo
import config

engine = config.PG_ENGINE

# Function for Twitter authentication
def authenticate():
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

# Function for streaming tweets
class TwitterListener(StreamListener):
    #defines what is done with every single tweet as it is intercepted in real-time
    def on_data(self, data):
        t = json.loads(data)

        tweet = {
        #user = api.get_user('spacy_io')
        'username': t['user']['screen_name'],
        'text': t['text'],
        'followers_count': t['user']['followers_count'],
        'location':t['user']['location'],
        'description':t['user']['description']
        }

        #
        logging.warning(f'\n\n\nTWEET! {tweet["username"]} just tweeted: "{tweet["text"]}"\n\n\n')
        
        # Insert the tweets into the mongo db
        db.tweets_db.insert_many(tweet)
        

    # Return an error if twitter is unreachable
    def on_error(self, status):
        if status == 420:
            print(status)
            return False


# Driver function
if __name__ == '__main__':
    client = pymongo.MongoClient(host='mongo_container', port=27018)
    db = client.tweets_db
    #collection = db.tweets
    #collection.insert_many(tweet["text"])    
    
    
    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['OnThisDay'], follow=['2278940227'], languages=['en'])
    #return tweets in English that contain 'on this day' or are posted by me (for testing)