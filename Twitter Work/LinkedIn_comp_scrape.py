from bs4 import BeautifulSoup
import pandas as pd
import requests
from random import randint
import time

start_time = time.time()

sleeper = randint(1,2)

url_template = "https://www.linkedin.com/jobs/jobs-in-united-states?location=United%20States&pageNum=1&position=1&trk=jobs_jserp_pagination_1&start={}"
i=0
df= pd.DataFrame()
for start in range(1,100000):
    start = (start-1) * 25 
    url = url_template.format(start)
    html = requests.get(url)
    time.sleep(sleeper)
    soup = BeautifulSoup(html.content, 'lxml')
    elements = soup.find_all('div', {'class': 'listed-job-posting__content jobs-search-result-item__content'})
    for elem in elements:
        company= elem.find('h4', {'class': 'listed-job-posting__company'}).text.strip()
        df = df.append({"company":company}, ignore_index=True)
        df = df.drop_duplicates()

        i+= 1
        if i % 1000 == 0:  
            print('You have ' + str(i) + ' results. ' + str(len(df)) + " of these are good.")
        
        if len(df) >= 100000:
            break
end_time = time.time()
print("DONE! It took :", (end_time- start_time)/60,"mins", "to finish")
