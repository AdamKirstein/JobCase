# need to grab all people with CDL from Facebook.
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

#prepare linkedin login creads
usr=input('Enter Email Id:')
pwd=input('Enter Password:')

#setup Chrome drvier
option = webdriver.ChromeOptions()
#adding incognito 
option.add_argument('— incognito')

#establishing the driver 
browser = webdriver.Chrome(executable_path='/Users/adamkirstein/Downloads/chromedriver', chrome_options=option)
#connecting browser to linked
browser.get("https://www.linkedin.com")

print("Opened linkedin")

#resting 1 second to appear human :P
sleep(time_delay)

#entering login creds 
username_box = browser.find_element_by_class_name('login-email')
username_box.send_keys(usr)
print ("Email Id entered")
sleep(time_delay)

password_box = browser.find_element_by_class_name('login-password')
password_box.send_keys(pwd)
print ("Password entered")
# sleep for 0.5 seconds
sleep(time_delay)

#sending login creds
login_box = browser.find_element_by_xpath('//*[@type="submit"]')
login_box.click()
# sleep for 0.5 seconds
sleep(time_delay)
print('Logged in ')

#querying nav bar to get to results page
navigation_bar = browser.find_element_by_class_name("nav-search-bar")
navigation_bar.click()
print('nav bar selected')

query_button = browser.find_element_by_class_name('nav-search-controls')
query_button.click()
print('query made')
sleep(time_delay)

#selecting 'More' button to toggle drop-down for companies
try:
    click_more = browser.find_element_by_class_name("search-vertical-filter__dropdown-trigger-text")

except:
    click_more = browser.find_element_by_xpath("//span[@class='search-vertical-filter__dropdown-trigger-text']")
click_more.click()


sleep(time_delay)

#navigating to first page of scrape. 
click_company = browser.find_element_by_xpath("//li[@class='search-vertical-filter__dropdown-list-item p0']")
click_company.click()
print("navigated")
sleep(time_delay)




### START OF SCRAPE ###
#zoom out of page and press space 2 times to load all companies. 
browser.execute_script("document.body.style.zoom='50%'")

actions = ActionChains(browser)
for _ in range(2):
    actions.send_keys(Keys.SPACE).perform()
sleep(3)
#create empty df to hold results
comp_df = pd.DataFrame()
#counter to control loop (also appending i to end of url to make it go to next page)
i = 1#start at one because page 1 =1 so if you start at 0 you will scrape the first page twice. 
item_names=[]
while True:
    #select the elements for the target titles
    titles = WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'h3[class="search-result__title t-16 t-black t-bold"]')))
    #iterate through the html of titles and append
    for title in titles:
        item_names.append(title.text)
        df = comp_df.append(item_names)
      #push i forward (making page go from one to 2)  
    i+=1
    try:
        #repeat the zoom and space for each new page because chrome is dumb and wont keep the page zoomed
        browser.execute_script("document.body.style.zoom='50%'")
        sleep(4)
        actions.send_keys(Keys.SPACE).perform()
        sleep(4)
        browser.get("https://www.linkedin.com/search/results/companies/?origin=SWITCH_SEARCH_VERTICAL&page="+str(i)+'')
        sleep(3)
    except:
        #stop scraper when ~= 100 (all pages will have been scraped)
        if i >= 100:
            break

    
    
print ("Done")
input('Press anything to quit')
browser.quit()
print("Finished")
