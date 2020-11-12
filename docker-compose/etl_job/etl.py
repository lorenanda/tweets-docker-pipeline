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
engine = create_engine('postgres://postgres:xxxx@postgres_container:5432/postgres')

# connect to MongoDB 
client = pymongo.MongoClient(host='mongodb', port=27018)
db = client.tweets_db

# Extract tweets from MongoDB
tweetsList = db.find()
for item in tweetsList:

## Transform the data
# clean text
text = re.sub('(RE:@[\w_]+)', "", text)

# sentiment analysis
sia = SentimentIntensityAnalyzer()
for tweet in tweets:
    tweet_sentiment = sia.polarity_scores(tweet)
    for score in tweet_sentiment:
        print('{0}: {1}, '.format(score, tweet_sentiment[score]), end='')


## Load the data into Postgres
create_query = """
CREATE TABLE IF NOT EXISTS tweets (
text VARCHAR(280)
);
"""
insert_query = f"INSERT INTO tweets VALUES (text) VALUES ('{tweet['text']}', '');"
engine.execute(insert_query) 