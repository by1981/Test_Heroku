
# coding: utf-8

# ## Complimenter

# In[ ]:


# Dependencies
import tweepy
import json
from config import consumer_key, consumer_secret, access_token, access_token_secret


# In[ ]:


# Twitter API Keys
consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_token_secret = access_token_secret


# In[ ]:


# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[ ]:


# Create a complimentary status update with a mention to another user
#api = tweepy.API(auth)
api.update_status("Happy Tuesday!!")

