
# coding: utf-8

# In[1]:


import requests as req


# In[2]:


res = req.get('https://www.colorado.gov/news')


# In[3]:


res


# In[4]:


#Called beautiful soup package
from bs4 import BeautifulSoup as bs

soup = bs(res.content)


# In[5]:


#Using beautiful soup to find all the view-page-item tag in a class of div
divs = soup.find_all('div', {'class': 'view-page-item'})


# In[6]:


type(divs[0])


# In[7]:


divs[0]


# In[8]:


#Shows the lenght of Dive
len(divs)


# In[9]:


#Returns the text
divs[0].text


# In[10]:


#display date text
divs[0].find('span' , {'class' : 'date-display-single'}).text


# In[11]:


import pandas as pd


# In[12]:


#Convert the date string to date time format
pd.to_datetime(divs[0].find('span' , {'class' : 'date-display-single'}).text)


# In[13]:


BASE_URL = 'https://www.colorado.gov/'


# In[14]:


divs[0].find('a')


# In[15]:


divs[0].find('a').text


# In[16]:


divs[0].find('a').get('href')


# In[17]:


#loop through the data in the divs
for d in divs:
    date = pd.to_datetime(d.find('p', {'class': 'date-display-single'}.text))
    link = d.find('a')
    href = link.get('href')
    title = link.text


# In[18]:


title


# In[19]:


date


# In[20]:


link


# In[21]:


@Note, i didnt have to use a base url because my herf gave full url link
href


# In[ ]:


from pymongo import MongoClient
from tqdm import tqdm_notebook

PAGE_URL = 'https://www.colorado.gov/news?page={}'

client = MongoClient()
db = client['news']
coll = db['colorado']

#loop through the 80 pages. I used range from 1-81 to count the 80 pages.
#I save all into the mondodb
for page in tqdm_notebook(range(1, 81)):        
    url = PAGE_URL.format(page)
    res = req.get(url)
    soup = bs(res.content)
    divs = soup.find_all('div', {'class': 'view-page-item'})
    date = pd.to_datetime(divs[0].find('span' , {'class' : 'date-display-single'}).text)
    for d in divs:
        #date = pd.to_datetime(d.find('p', {'class': 'date-display-single'}).text)
        link = d.find('a')
        href = link.get('href')
        title = link.text
        
        coll.insert_one({'date': date,
                        'link': href,
                        'title': title})

client.close()


# In[46]:


from pprint import pprint

client = MongoClient()
db = client['news']
coll = db['coloradoNews']

pprint(coll.find_one())


# #        PART 2

# # WEEK 6 LAB ASSIGNMENT: BONUS QUESTION

# Objective: WebScrapping csv from  MISO database.

# In[2]:


#urllib request is a Python module for fetching URLs.
import urllib.request
# from Market Report directories,
# For day-ahead pricing:
# 'https://docs.misoenergy.org/marketreports/YYYYMMDD_da_pr.xls'
#I use the curl brackets to format the date to year, month and day
DL_link = 'https://docs.misoenergy.org/marketreports/{}{}{}_da_bc.xls'
formatted_link = DL_link.format('2020', '06', '10')


# In[3]:


#Extract the link
formatted_link


# In[4]:


#Using the command below gives the tuple of the file name and the server response
urllib.request.urlretrieve(formatted_link, '20200610_da_bc.xls')


# In[5]:


#I listed the file in my directory, opened and saved it in jupiter lab location
ls


# In[ ]:


# Used Pandas to read the file and do some data cleaning before saving into the mongodb.
#I converted the excel into csv becuause i had issues installing xlrd package which i could used to convert xls file.
#I skipped the first 3 rows and started from the main header


# In[6]:


import numpy as np # linear algebra
import pandas as pd
xls = pd.read_csv("20200610_da_bc.csv",skiprows=3)
xls


# In[7]:


#I drop 3 columns namely 'Flowgate NERC ID', 'Constraint Description','Reason' becuae they have no records
df = xls.drop(['Flowgate NERC ID', 'Constraint Description','Reason'], axis = 1) 
df


# In[8]:


#Initilise mongo client
from pymongo import MongoClient


# In[9]:


# define connection for Mongo to match database and collection created
client = MongoClient()
db = client['misoenergy']
collection = db['Year2020']


# In[10]:


df.to_dict('records')


# In[11]:


#Insert whole data into our collection created
collection.insert_many(df.to_dict('records'))


# In[12]:


# show an example
collection.find_one()


# In[13]:


# show an example for 10 records
df = collection.find().limit(10)


# In[14]:


# print 10 records from database
for data in df:
    print(data)

