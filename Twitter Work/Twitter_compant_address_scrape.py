#not functional just yet. Still in development 

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from random import randint
import requests
import pandas as pd
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

time_delay = randint(3,6)

#setup Chrome drvier
option = webdriver.ChromeOptions()
#adding incognito 
option.add_argument('— incognito')

#establishing the driver 
browser = webdriver.Chrome(executable_path='/Users/adamkirstein/Downloads/chromedriver', chrome_options=option)


# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
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

for i in comp:
    search_query.send_keys('i')
    search_query.send_keys(Keys.RETURN)


# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)
