# Jobcase

my solution for Jobcase's challenge to:

1. create a webscraper that can collect 100,000 job listings from indeed and store them.
   - Considers approaches using multiple types of webscraper packages, (Bs4, Selenium, Node.js puppeteer)
   - focuses on trying to reduce time per scrape. 
   - findings suggested that using lxml parser improved speed, as did using css selectors to locate attributed. Javscript-based scrapers, (Node.js and Selenium) proved to crawl more pages per hour than did bs4. 
   - project next steps: multip-processing, addtional tweaks to scrapers. 

2. conduct a sentiment analysis of tweets for 100,000 companies using the the twitter API (tweepy)
  - uses tweepy streaming to collect and store tweets related to a list of companies sourced and compiled through different online channels, using both webscraping, and publicly available datasets. 
  - feeds tweepy each company name, and outputs lists of tweets containing those names. Tweets are composed of company brodcasts, reviews, customer service requests, events, debates, and more. As tweets stream in, TextBlob performs automated sentiment analysis using key words in the text for classification. 
  - pushes live-stream tweets, and sentiment to sqllite db, after which company names are mapped to the tweets in python. 
  - Additional deep-dive analysis is then carried out on compiled db. 



