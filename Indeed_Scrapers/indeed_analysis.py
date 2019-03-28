import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import re

#reading in indeed scrpaed data
df = pd.read_csv('indeed_jobs_final.csv')

df.drop(df.columns[[0,1]], axis=1, inplace=True)

#filtering out fulltime
df= df[df.job_type =='fulltime']

#df.salary.value_counts()
gr = df.groupby("salary").agg('count')

plt.rcParams.update({'font.size': 20})

df.dropna(inplace=True)
counts = df["company_name"].value_counts().head()
fig, ax0 = plt.subplots(figsize=(15, 7))

#Plotting Companies
ax0.bar(range(len(counts)), counts)
#ax0.set_xticklabels(counts.index, rotation=45)
ax0.set_title('Most Common Full Time Compensation')
plt.title("Companies With Most Opportunity")
plt.xlabel("Company")
plt.show()
print(counts)
plt.show()

#plottting job title
counts = df["job_title"].value_counts().head()
counts.index = counts.index.str.split('-').str[0]
fig, ax0 = plt.subplots(figsize=(40, 10))


ax0.bar(range(len(counts)), counts)
#ax0.set_xticklabels(counts.index, rotation=45)
ax0.set_title('Most Sought jobs')
plt.title("Most Sought jobs")
plt.xlabel("Job")
plt.ylabel("Job Count")
plt.show()
print(counts)
plt.show()

#plotting location
counts = df1["Location"].value_counts().head()
counts.index = counts.index.str.split('-').str[0]
fig, ax0 = plt.subplots(figsize=(40, 10))


ax0.bar(range(len(counts)), counts)
#ax0.set_xticklabels(counts.index, rotation=45)
ax0.set_title('Most Sought jobs')
plt.title("Locations with most opportunity")
plt.xlabel("Location")
plt.ylabel("Locale Count")
plt.show()
print(counts)
plt.show()
