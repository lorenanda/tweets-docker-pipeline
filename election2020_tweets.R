'''
How do people feel about the (outcome of the) US Election?
Sentiment analysis of #Election2020 tweets
code adapted from https://uvastatlab.github.io/2019/05/03/an-introduction-to-analyzing-twitter-data-with-r/
'''

# Import the necessary libraries
library(twitteR)
library(ROAuth)
library(httr)
library(base64enc)
library(dplyr)
library(plyr)
library(dismo)
library(maps)
library(tidyverse)
library(tidytext)
library(lubridate)
library(ggplot2)

# Setup the keys/tokens of your registered Twitter app
api_key = ""
api_secret = ""
access_token = ""
acces_token_secret = ""

download.file(url="http://curl.haxx.se/ca/cacert.pem", destfile = "cacert.pem")

setup_twitter_oauth(api_key, api_secret, access_token, acces_token_secret)

# Set the wanted twitter hashtag and number of tweets to be returned
search.string <- "#Election2020"
no.of.tweets <- 1000
election_tweets <- searchTwitter(search.string, n=no.of.tweets, lang="en") # Search only tweets in English

# Create a dataframe of the tweets
election_tweets_df <- do.call("rbind", lapply(election_tweets, as.data.frame))
View(election_tweets_df)

election_tweets_df$created <- as.Date(election_tweets_df$created, format= "%y-%m-%d")
election_tweets_df$text <- as.character(election_tweets_df$text)

# Plot the distribution of tweets per day
election_tweets_df$date <- day(election_tweets_df$created)
ggplot(election_tweets_df, aes(x = date)) + geom_density()

### Clean text
election_tweets_df$text <- gsub("@[[:alpha:]]*","", election_tweets_df$text)

# Convert the text into a corpus object
library(tm)
text_corpus <- Corpus(VectorSource(election_tweets_df$text))

text_corpus <- tm_map(text_corpus, tolower)
text_corpus <- tm_map(text_corpus, removeWords, c("election", "rt", "re", "amp"))
text_corpus <- tm_map(text_corpus, removeWords, stopwords("english"))
text_corpus <- tm_map(text_corpus, removePunctuation)
text_df <- data.frame(text_clean = get("content", text_corpus), stringsAsFactors = FALSE)
election_tweets_df <- cbind.data.frame(election_tweets_df, text_df)


### Sentiment analysis
library(SentimentAnalysis)
election_sentiment <- analyzeSentiment(election_tweets_df$text_clean)

election_sentiment <- dplyr::select(election_sentiment, 
                                 SentimentGI, SentimentHE,
                                 SentimentLM, SentimentQDAP, 
                                 WordCount)

election_sentiment <- dplyr::mutate(election_sentiment, mean_sentiment = rowMeans(election_sentiment[,-5]))
election_sentiment <- dplyr::select(election_sentiment, WordCount, mean_sentiment)
election_tweets_df <- cbind.data.frame(election_tweets_df, election_sentiment)


# Nr of positive and negative tweets
pos_tweets <- nrow(election_tweets_df[election_tweets_df$mean_sentiment > 0, ])
neg_tweets <- nrow(election_tweets_df[election_tweets_df$mean_sentiment < 0, ])
tweet_sentiments <- c(pos_tweets, neg_tweets)
barplot(tweet_sentiments, 
        main="Tweets about the 2020 US Election outcome", 
        xlab="Sentiment",
        ylab="Number of tweets",
        names.arg=c("positive","negative"),
        col="blue")

### Topic identification
library(quanteda)

election_tokenized <- tokens(election_tweets_df$text_clean)
election_dfm <- dfm(election_tokenized)
word_sums <- colSums(election_dfm)
length(word_sums)

freq_data <- data.frame(word = names(word_sums), 
                        freq = word_sums, 
                        row.names = NULL,
                        stringsAsFactors = FALSE)

sorted_freq_data <- freq_data[order(freq_data$freq, decreasing = TRUE), ]

election_tm <- Corpus(VectorSource(election_tweets_df[,19]))

election_dtm <- DocumentTermMatrix(election_tm)
election_dtm <- removeSparseTerms(election_dtm, 0.98)

election_df_cluster <- as.data.frame(as.matrix(election_dtm))

# Visualization
library(devtools)
# devtools::install_github("hfgolino/EGA")
library(EGA)

ega_election <- EGA(election_df_cluster)