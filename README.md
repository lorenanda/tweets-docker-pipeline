# Tweet streaming pipeline for a Slackbot
This project was completed in week 7 of the Data Science Bootcamp at Spiced Academy in Berlin.

![pipeline](https://github.com/lorenanda/tweets-docker-pipeline/blob/main/ETL_pipeline.png)

## Description
The goal of this project is to create a database of tweets that use the hashtag #OnThisDay along with their sentiment score, and post a tweet in a Slack channel, to inform members about historical events that happened on that day.

The Docker-Compose pipeline includes five steps (containters):
1. Collect tweets using the Twitter API and tweepy (`tweet_collector`)
2. Store the tweets in a MongoDB
3. Apply ETL job (`etl_job`)
  - Extract tweets from MongoDB.
  - Clean the text and apply sentiment analyis with VADER/TextBlob.
4. Load the cleaned tweet texts and their sentiment scores in a Postgres database.
5. Create a Slackbot that post a randomly selected tweet from the Postgres database into a Slack channel (`slackbot`)

You can read about the workflow in more detail in [this blog post](https://lorenaciutacu.com/2020-11-14-bootcamp7/).
