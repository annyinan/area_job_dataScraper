# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import urllib
import pandas as pd
from random import randint
from time import sleep
import re

no_pages=1
job_titles=list()  
companies=list()
location=list()
summary=list()
prov=list()
summ_link=list()

provinces=list()
#provinces.append('British+Columbia')
provinces.append('Alberta')
provinces.append('Prince+Rupert')
provinces.append('Terrace')
provinces.append('Smithers')
provinces.append('Burns+Lake')
provinces.append('Prince+George')
provinces.append('Valemount')
#provinces.append('Saskatchewan')
#provinces.append('Manitoba')
#provinces.append('Ontario')
#provinces.append('Quebec')
#provinces.append('New+Brunswick')
#provinces.append('Nova+Scotia')
#provinces.append('Prince+Edward+Island')
#provinces.append('Newfoundland+and+Labrador')
#provinces.append('Yukon')
#provinces.append('Northwest+Territories')
#provinces.append('Nunavut')

for j in provinces:
    i=0
    while i/25<no_pages:
        ##link='https://www.indeed.ca/jobs?l=Alberta&start='+str(i)
        link='https://www.indeed.ca/jobs?l='+j+'&start='+str(i)
        source_code=urllib.request.urlopen(link)    
        soup=BeautifulSoup(source_code,'html.parser')     
        titles=soup.find_all('a',{'data-tn-element':['jobTitle']})
        for x in titles:
            job_titles.append(x.text.strip())
            summ_link.append(x.get('href'))
            prov.append(j)
        comp=soup.find_all('span', {'class':['company']})
        for x in comp:
            companies.append(x.text.strip())        
        loc=soup.find_all(['div','span'], {'class':['location']})
        for x in loc:
            location.append(x.text.strip())               
        i=i+25

for h in range(0,len(job_titles)):       
    desc_link='https://www.indeed.ca'+summ_link[h]
    desc_code=urllib.request.urlopen(desc_link)    
    desc_soup=BeautifulSoup(desc_code,'html.parser').find('div',{'class':['jobsearch-JobComponent-description']})
    if hasattr(desc_soup,'text')==False:
        summary.append('No description available')
    else:
        summary.append(desc_soup.text.strip())
    sleep(randint(0,5))
    
for x in range(0,len(job_titles)):
    summary[x]=summary[x].replace('\n','')   
    summary[x]=re.sub(r"([a-z,!,.,:,?])([A-Z])",r"\1 \2", summary[x])
 
    
df=pd.DataFrame(
        {'job_title':job_titles,
         'provinces':prov,
         'location':location,
         'job_description':summary
         }, index=None)
    
df.to_csv('JobData.csv')


del companies
del job_titles
del link
del location
del summary
del i 
del j
del h
del summ_link
del no_pages
del prov
del provinces  
del desc_link
del desc_soup
del df




