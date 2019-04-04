import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import pandas as pd 
import csv #Import csv
from tweepy import Cursor
from datetime import datetime, date, time, timedelta


#logging into twitter
consumer_key = "HwXXXXXXXXXXXX"
consumer_secret = "eEXXXXXXXXXXXXXXXXXR"
access_token = "XXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXX"
# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth,timeout=60, wait_on_rate_limit=True)

#reading in list of companies
dfcompanies = pd.read_csv("companies_twitter.csv")

dfcompanies.COMPANIES= dfcompanies.COMPANIES.astype(str)

dfcompanies.COMPANIES = dfcompanies.COMPANIES.replace('\t','', regex=True)

dfcompanies.COMPANIES = ('@' + dfcompanies.COMPANIES)

comp_list = dfcompanies.COMPANIES.astype(str).values.tolist()
#testing with 10 companies 
#comps = comp_list[:100]


#setting up stream listener to collect tweets and handle errors. 
class StreamListener(tweepy.StreamListener):

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def on_status(self, status):
        if status.retweeted:            
            return
        text = status.text
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
        positive = polarity  >0
        negative =  polarity<0
        neutral = polarity ==0
    
        table = db["total_twitter_set"]
        table.insert(dict(
            text=text,
            polarity=sent.polarity,
            subjectivity=sent.subjectivity,
            positive = positive, 
            negative = negative ,
            neutral = neutral
        ))
        print(status.text)
        def on_error(self, status_code):
            if status_code == 420:
                return False
  
#extracting the id codes from the company names list 
#for i in comp_list:
  #  try: 
   #     users = api.get_user(i)
  #  except: 
  #      continue
    #print(users.id)
                
 #building sqlite db              
import dataset
db = dataset.connect("sqlite:///total_twitter_set.db") 

#reading in csv holding newly extracted ids
ids = pd.read_csv('company_ids.csv')
ids["company ids"] = ids["company ids"].astype(int)
ids = ids["company ids"].astype(str).values.tolist()

#execute 
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
#switching 'track' to 'follow' to monitor mentions of the company ids. (able to go through more in a better, faster way
stream.filter(follow=[i for i in ids] ,languages=["en"])
    
    
 #testing db access and population 
import sqlite3
conn = sqlite3.connect("total_twitter_set.db")

cur = conn.cursor()
df = pd.read_sql_query("select * from total_twitter_set ;", conn)


