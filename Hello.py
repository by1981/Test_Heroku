
# coding: utf-8

# ## Complimenter

# In[ ]:

from os import environ

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
#from config import consumer_key, consumer_secret,  access_token, access_token_secret
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# In[ ]:
#import os
# is_prod = os.environ.get('IS_HEROKU', None)

# if is_prod:

# Twitter API Keys
consumer_key = environ['Twitter_consumer_key']
consumer_secret = environ['Twitter_consumer_secret']
access_token = environ['Twitter_access_token']
access_token_secret = environ['Twitter_access_token_secret']


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
    sentiments = []
    for status in tweepy.Cursor(api.search, q=target_user,tweet_mode="extended").items(500):
        tweet = status._json
        compound = analyzer.polarity_scores(tweet["full_text"])["compound"]
        pos = analyzer.polarity_scores(tweet["full_text"])["pos"]
        neu = analyzer.polarity_scores(tweet["full_text"])["neu"]
        neg = analyzer.polarity_scores(tweet["full_text"])["neg"]
        
        
    # Add sentiments for each tweet into an array
        sentiments.append({"Date": tweet["created_at"], 
                       "Compound": compound,
                       "Positive": pos,
                       "Negative": neu,
                       "Neutral": neg,
                        "Tweets Ago": tweet_number,
                          "Tweet_text": tweet["full_text"],
                          "username_1": tweet['user']['name']})

    sentiments_pd = pd.DataFrame.from_dict(sentiments)
    #plt.legend(sentiments_pd["username_1"],mode="expand", title="Tweets")
    plt.figure(figsize=(9,7))
    plt.legend((tweet['user']['screen_name']))
    plt.title("Sentiment Analysis of Tweets (%s) for %s" % (time.strftime("%x"), target_user))
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    plt.plot(np.arange(len(sentiments_pd["Compound"])),
         sentiments_pd["Compound"], marker="o", linewidth=0.5,
         alpha=0.8)
    plt.legend(sentiments_pd[username_1],loc='upper right', title="Tweets")
    plt.grid()
    ax = plt.gca().invert_xaxis()
    plt.savefig('Sentiment Analysis.png')
    api.update_with_media("Sentiment Analysis.png")
    plt.clf()
repeater=0

while(True):

    # Call the TweetQuotes function and specify the tweet number
    TweetOut(repeater)
    

    # Once tweeted, wait 60 seconds before doing anything else
    time.sleep(60)

    # Add 1 to the counter prior to re-running the loop
    repeater = repeater + 1

