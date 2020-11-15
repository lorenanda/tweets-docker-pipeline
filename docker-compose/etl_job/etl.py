# Run this from within Docker
import pymongo
from sqlalchemy import create_engine
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import config
import tweet_streamer

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
client = config.LOCAL_CLIENT
db = client.tweets_db

# Extract tweets from MongoDB
find_tweets  = db.tweets_collection.find({})
for tweet in find_tweets:
    #clean text
    tweet_text = tweet['text'].replace("\'","")

    #sentiment analysis
    sia = SentimentIntensityAnalyzer()
    tweet_sia = sia.polarity_scores(tweet_text)['compound']
    tweet_blob = TextBlob(tweet_text).sentiment

    # Print out the extracted tweet
    logging.critical(f'Tweet extracted: {tweet_text}')

    ## Load the data into Postgres
    insert_query = """
    INSERT INTO tweets (text, sia_score, blob_score)
    VALUES ('{tweet_text}, {tweet_sia}, {tweet_blob});
    """
    engine.execute(insert_query)
