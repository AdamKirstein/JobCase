# load the library
from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
import re
import time
# indeed.com url
base_url = 'https://www.indeed.com/jobs?q=all+jobs+hiring&jt={}&l=Anywhere&sort={}&start={}'
sort_by = 'date'          # sort by data
#start_from = '&start='    # start page number
#pd.set_option('max_colwidth',500)    # to remove column limit (Otherwise, we'll lose some info)
df = pd.DataFrame()   # create a new data frame


start_time = time.time()
jobtype= ['fulltime','parttime']
i = 0
for job in jobtype:
    for page in range(1,5002): # page from 1 to 100 (last page we can scrape is 100)
        page = (page-1) * 10  
        url = base_url.format(job,sort_by,page)
        html = requests.get(url)
        time.sleep(1)
        soup = Soup(html.content, 'lxml')
        soupelements = soup.find_all(class_= "result" )
        for elem in soupelements: 
            #get job title
            try:
                job_title = elem.find('a', attrs={'class':'turnstileLink'}).attrs['title']
            except:
                job_title=None
            #get company name
            try:
                comp_name = elem.find(class_='company').text.replace('\n', '')
            except:
                comp_name=None
                
            #get date of post
            try:
                job_posted = elem.find('span', attrs={'class': 'date'}).getText()
            except: 
                    None
            #get salary        
            try:
                salary = elem.find('span', {'class':'no-wrap'}).text
            except:
                salary= None
            #determine if job is fulltime or parttime
            job_type = job  
            #get url and href     
            home_url = "http://www.indeed.com"
            job_link = "%s%s" % (home_url,elem.find('a').get('href'))

            try:
                synopsis= elem.find('span', {'class':'summary'}).text.replace('\n', '')
            except: 
                synopsis = None
            #compile all into d
            df = df.append({'job_title': job_title,'company_name': comp_name,
                            'date_posted': job_posted,"salary": salary,'job_type':job_type,
                            "synopsis":synopsis, 'job_link': job_link}, ignore_index=True)
            i+= 1
            if i % 1000 == 0:  
                print(len(df),'You have ' + str(i) + ' results. ' + str(df.dropna().drop_duplicates().shape[0]) + " of these are good.")
            if len(df) >= 100000:
                break
end_time = time.time()
print("DONE! It took :", (end_time- start_time)/60,"mins", "to finish")
