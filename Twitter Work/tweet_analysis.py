import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import string
import nltk
import re
from nltk import word_tokenize
from nltk.stem.porter import *
from wordcloud import WordCloud
from matplotlib.pyplot import figure
from pylab import rcParams

pd.set_option('max_colwidth',1000) 
tweets = pd.read_csv("tweets.csv")
#tweets.head()

#list of companies 
comp = ['@IBM',
 '@Hewlett Packard Enterprise',
 '@HP',
 '@Microsoft',
 '@Dell',
 '@Procter & Gamble',
 '@Pfizer',
 '@GE',
 '@Johnson & Johnson',
 '@JPMorgan Chase & Co.']

#mapping companies to their tweets
def get_companies(row):
    companies = []
    text = row["text"].lower()
    if "@ibm" in text:
        companies.append("IBM")
    if "@hewlett packard enterprise" in text or "@hp" in text:
        companies.append("HP")
    if "@microsoft" in text:
        companies.append("Microsoft")
    if "@dell" in text:
        companies.append("Dell")
    if "@proctor & gamble" in text or "@p&g" in text:
        companies.append("Dell")
    if "@pfizer" in text:
        companies.append("Pfizer")
    if "@ge" in text or "general electric" in text:
        companies.append("GE")
    if "@johnson & johnson" in text:
        companies.append("Johnson & Johnson")
    if "@jpmorgan Chase & Co." in text or "@jp morgan" in text:
        companies.append("JP Morgan")
    return ",".join(companies)
tweets["companies"] = tweets.apply(get_companies,axis=1)

#filtering tweets fohttp://localhost:8888/notebooks/Documents/Twitter%20Scraping/Tweet%20exploration%20.ipynb#r companies as indiviuals, preventing from values like Micosoft,GE,Dell for example. 
tweets = tweets.loc[(tweets['companies'] == "GE") | (tweets['companies'] == "Microsoft")| (tweets['companies'] =="IBM")| (tweets["companies"]=="Dell")| (tweets['companies'] =="Pfizer")]

#viz of company presence
plt.rcParams.update({'font.size': 22})
rcParams['figure.figsize'] = 20, 10
tweets.groupby("companies").agg({'companies':'count'}).plot(kind='bar',legend=None,title = "Presence of Companies in tweets")


#creatting a broken down filter of polarity
tweets["positive"] = tweets.polarity > 0
tweets['negative'] = tweets.polarity < 0 
tweets['neutral'] = tweets.polarity == 0

#proportion of negative tweets for microsoft viz
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.subplots(figsize=(20, 7))
plt.title('Total Negative Tweets ')
tweets.groupby("companies")["negative"].sum().plot(kind='bar')

#Overview of rating proportion 
tweets.negative.sum()

tweets.positive.sum()

tweets.neutral.sum()

#Focusing on Microsoft for its high negative rating. 
microdf = tweets[tweets.companies == "Microsoft"]
microdf = microdf[microdf.polarity <0]

microdf.reset_index(drop=True, inplace=True)

#grouping companies and getting overview of how each company has performed
tweet_agg = tweets.groupby('companies').agg({'positive': 'sum', 'negative': 'sum', 'neutral':'sum'})
#tweet_agg

#setting up text for analysis
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt

#cleaning up the text
#removing @
microdf['tidy_tweet'] = np.vectorize(remove_pattern)(microdf['text'], "@[\w]*")
#removing special characters
microdf['tidy_tweet'] = microdf['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
microdf = microdf[~microdf['tidy_tweet'].str.contains("Maersk")]
microdf = microdf[~microdf['tidy_tweet'].str.contains("https")]

#removing small words like hmmm, and oh. 
microdf['tidy_tweet'] = microdf['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
#tokenized_tweet = microdf['tidy_tweet'].apply(lambda x: x.split())
#tokenized_tweet.head()

#tokenizing texts
tokenized_tweet = microdf['tidy_tweet'].apply(lambda x: x.split())
stemmer = PorterStemmer()
tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming

#tokenized_tweet

#breaking everything down to all words, completely unstructured
all_words = ' '.join([text for text in microdf['tidy_tweet']])

#building wordcloud
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
