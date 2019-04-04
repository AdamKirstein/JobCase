# load the library
from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
import re
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String,Integer
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column


# indeed.com url
base_url = 'https://www.indeed.com/jobs?q=all+jobs+hiring&jt={}&l=Anywhere&sort={}&start={}'
sort_by = 'date'          # sort by data
#start_from = '&start='    # start page number
#pd.set_option('max_colwidth',500)    # to remove column limit (Otherwise, we'll lose some info)
df = pd.DataFrame()   # create a new data frame




#init base
Base = declarative_base()


#create Schema for DB     
class PostInfo(Base):
    __tablename__ = 'postInfo'
    id = Column(Integer, primary_key=True)
    company = Column(String(1000))
    job = Column(String(1000))

class Location(Base):
    __tablename__ = 'job_location'
    id = Column(Integer, primary_key=True)
    locations = Column(String(1000))


class JobType(Base):
    __tablename__ = 'job_type'
    id = Column(Integer, primary_key=True)
    jobtType =  Column(String(1000))


class Compensation(Base):
    __tablename__ = 'compensation'
    id = Column(Integer, primary_key=True)
    salary = Column(String(1000))
    
#main sceh
class main_table(Base):
    __tablename__ = 'job_post'
    id = Column(Integer, primary_key=True)
    dateposted = Column(String(50), nullable=False)
    URL = Column(String(1000))
    description = Column(String(5000))
    
    company_id = Column(Integer, ForeignKey('postInfo.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('postInfo.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('job_location.id'), nullable=False)
    jobtType_id = Column(Integer, ForeignKey('job_type.id'), nullable=False)
    salary_id = Column(Integer, ForeignKey('compensation.id'), nullable=False)

engine = create_engine('sqlite:///jobcase_indeed.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#apply db class attributes to data points and push

jobtype= ['fulltime','parttime']
i = 0
for job in jobtype:
    for page in range(1,10): # page from 1 to 100 (last page we can scrape is 100)
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
                final_job = PostInfo(job= job_title)
                session.add(final_job)
            except:
                pass
            
            #get company name
            try:
                comp_name = elem.find(class_='company').text.replace('\n', '')
                final_comp_name = PostInfo(company=comp_name)
                session.add(final_comp_name)

            except:
                pass
                
            #get date of post
            try:
                job_posted = elem.find('span', attrs={'class': 'date'}).getText()
                final_date = main_table(dateposted=job_posted)
                session.add(final_date)
            except: 
                    pass
            #get salary        
            try:
                salary = elem.find('span', {'class':'no-wrap'}).text
                final_salary = Compensation(salary = salary)
                session.add(final_salary)
            except:
                pass
            #determine if job is fulltime or parttime
            
            try: 
                job_type = job  
                final_jobtype = JobType(jobtType = job_type )
                session.add(final_jobtype)
            except: 
                  pass
            
            
            #get url and href     
            home_url = "http://www.indeed.com"
            job_link = "%s%s" % (home_url,elem.find('a').get('href'))
            final_url = main_table(URL = job_link)
            session.add(final_url)

            try:
                synopsis= elem.find('span', {'class':'summary'}).text.replace('\n', '')
                final_synopsis = main_table(description = synopsis)
                session.add(final_synopsis)
            except: 
                pass
            try: 
                location = elem.find('div', {'class':'location'}).text
                final_location = Location(locations = location)
                session.add(final_location)
            except: 
                pass
            session.commit()
            i += 1
