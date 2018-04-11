
# coding: utf-8

# ## Complimenter

# In[ ]:


# Dependencies
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import json
import tweepy
from datetime import datetime
import time
from config import consumer_key, consumer_secret,  access_token, access_token_secret
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# In[ ]:


# Twitter API Keys
consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_token_secret = access_token_secret


# In[ ]:

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# Setup Tweepy API Authentication


# In[ ]:


# Create a complimentary status update with a mention to another user
#api = tweepy.API(auth)
target_user = "@CNN"
def TweetOut(tweet_number):
    counter = 1
    sentiments = []
    for status in tweepy.Cursor(api.search, q=target_user,tweet_mode="extended").items(100):
        tweet = status._json
    
    # Run Vader Analysis on each tweet
        compound = analyzer.polarity_scores(tweet["full_text"])["compound"]
        pos = analyzer.polarity_scores(tweet["full_text"])["pos"]
        neu = analyzer.polarity_scores(tweet["full_text"])["neu"]
        neg = analyzer.polarity_scores(tweet["full_text"])["neg"]
        tweets_ago = counter
        
    # Add sentiments for each tweet into an array
        sentiments.append({"Date": tweet["created_at"], 
                       "Compound": compound,
                       "Positive": pos,
                       "Negative": neu,
                       "Neutral": neg,
                        "Tweets Ago": tweet_number,
                          "Tweet_text": tweet["full_text"]})

    # Add to counter 
        counter = counter + 1
    sentiments_pd = pd.DataFrame.from_dict(sentiments)
    plt.title("Sentiment Analysis of Tweets (%s) for %s" % (time.strftime("%x"), target_user))
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    plt.plot(np.arange(len(sentiments_pd["Compound"])),
         sentiments_pd["Compound"], marker="o", linewidth=0.5,
         alpha=0.8)
    ax = plt.gca().invert_xaxis()
    plt.savefig('Sentiment Analysis.png')
    api.update_with_media("Sentiment Analysis.png")
    plt.clf()
    
repeater=0
while(True):

    # Call the TweetQuotes function and specify the tweet number
    TweetOut(repeater)

    # Once tweeted, wait 60 seconds before doing anything else
    time.sleep(20)

    # Add 1 to the counter prior to re-running the loop
    repeater = repeater + 1

    #THE END



