# Run this from within Docker
import pymongo
from sqlalchemy import create_engine
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import logging
#import config
#import tweet_streamer

time.sleep(5)

# connect to Postgres
engine = config.PG_ENGINE

create_query = """
CREATE TABLE IF NOT EXISTS tweets (
user VARCHAR,
text VARCHAR,
sia_score NUMERIC,
blob_score NUMERIC
);
"""
engine.execute(create_query)

# connect to MongoDB 
client = pymongo.MongoClient(host='mongodb', port=27017)
db = client.tweets_db


# Extract tweets from MongoDB
def extract_tweets():
    tweets  = list(db.onthisday.find())
    if tweets:
        t = random.choice(tweets)
        logging.critical("Random tweet: "+t["text"])
        return t


# Sentiment analysis
def transform_tweets(tweet):
    #clean text
    tweet_text = tweet['text'].replace("\'","")

    #sentiment analysis
    sia = SentimentIntensityAnalyzer()
    tweet_sia = sia.polarity_scores(tweet_text)['compound']
    tweet_blob = TextBlob(tweet_text).sentiment
    return tweet_sia


# Load the data into Postgres
def load_tweets(tweet, sentiment):
    insert_query = """
    INSERT INTO tweets VALUES ('{tweet["text"]}', {tweet_sia});
    """
    engine.execute(insert_query)
    # Print out the extracted tweet
    logging.critical(f'Tweet {tweet["text"]} loaded into Postgres.')



logging.critical("Starting ETL job")
while True:
    tweet = extract_tweets()
    if tweet:
        sentiment = transform_tweets(tweet)
        load_tweets(tweet, sentiment)
    time.sleep(10)