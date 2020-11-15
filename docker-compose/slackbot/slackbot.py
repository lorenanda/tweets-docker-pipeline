import sqlalchemy 
from sqlalchemy import create_engine
import config
import requests

engine = config.PG_ENGINE
webhook_url = config.WEBHOOK_SLACK

result = engine.execute("SELECT * FROM tweets;")

for row in result:
    output = f'NEW TWEET! {user} just tweeted: {text} \nSentiment score: {blob_score}'
    data = {'text':output}
    requests.post(url=webhook_url, json=data)

## TESTING
#example = ("TWEET! anne_obrien just tweeted: #OnThisDay in 1789 Benjamin Franklin writes 'Nothing . . . certain but death & taxes'")
#tweet_sentiment = TextBlob(example).sentiment
#tweet_sia = sia.polarity_scores(example)
#data = {'text': example, 'sentiment_blob':tweet_sentiment, 'sentiment_sia':tweet_sia}