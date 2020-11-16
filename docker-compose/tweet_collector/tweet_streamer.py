from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
import json
import logging
import pymongo
import config


client = pymongo.MongoClient(host='mongo_container', port=27018)
db = client.tweets_db

auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True)
user = api.me()
logging.critical("connection established with user: " + user.name)

# # Function for Twitter authentication
# def authenticate():
#     auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
#     auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
#     return auth

# Function for streaming tweets
class TwitterListener(StreamListener):
    #defines what is done with every single tweet as it is intercepted in real-time
    def __init__(self, limit, callback):
        #super().__init__()
        self.limit = limit
        self.counter = 0
        self.callback = callback

    # Return an error if twitter is unreachable
    def on_error(self, status):
        if status == 420:
            print(status)
            return False

    def get_tweets_dict(self, t):
        if 'extended_tweet' in t:
            text = t['extended_tweet']['full_text']
        else:
            text = t['text']

        tweet = {
        'username': t['user']['screen_name'],
        'text': t['text'],
        'followers_count': t['user']['followers_count'],
        'location':t['user']['location'],
        'description':t['user']['description']
        }

        return tweet

    def on_data(self, data):
        t = json.loads(data)
        tweet = self.get_tweet_dict(t)
        self.callback(tweet)
        self.counter += 1
        if self.counter == self.limit:
            return False


def stream_tweets(limit, callback):
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=['OnThisDay'], follow=['2278940227'], languages=['en'])

def warning_log(tweet):
    #logging.critical(f'\n\nTWEET! {tweet["username"]} just tweeted: "{tweet["text"]}"\n\n\n')
    logging.critical('\n\nTWEET: ' + tweet['username'] + 'just tweeted: ' + tweet['text'])
    db.collections.onthisday.insert_one(tweet)



# Driver function
if __name__ == '__main__':
    while True:
        stream_tweets(5, warning_log)
        time.sleep(30)