#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:44:37 2020

@author: revekka
"""

import sys
import os
import pandas as pd 
import string
import collections
from pathlib import Path


pathname = os.path.dirname(sys.argv[0]) 
path_name=os.path.abspath(pathname)
s='Name'
fname=os.path.join(path_name+ '/'+s+'_freq1.txt' )
my_file = Path(fname)
key='keyword_1'
   

def create_lst(fname, key, sector):
    text=open(fname, 'r+') #encoding='utf-8'   
    list_with_text = text.read().splitlines()
    #print(type(list_with_text[2]))
    #print(list_with_text)
    url, research, development, innovation, design, extra_info = ([] for i in range(0,6))
    #print(list_with_text[0])
    for link in range(0,len(list_with_text),11): #url
        #print(list_with_text[i])
        url.append(list_with_text[link])
        dump_list=[]
        for info in range(link+2,link+11,2):
            lst=list_with_text[info].strip('][').split(', ') 
            dump_list.append(lst[0])    
        research.append(dump_list[0])
        development.append(dump_list[1])
        innovation.append(dump_list[2])
        design.append(dump_list[3])
        #extra text
        extra=list_with_text[link+10]
        if extra=="[]":
            extra_info.append('')
        else:
            extra=extra.replace('\\u3000',' ').replace('\\u200b', ' ').replace('\\xa0', ' ').replace("\\u2028",' ').replace('\\xad', ' ').replace('\\u00ad', ' ')
            extra=extra.replace("  "," ").replace("\\n","").replace("\\r","").replace("\\t","")
            extra_info.append(x)
        
    # extract name from url
    company=[url[i].split('/')[2].split('.') for i in range(0,len(url))]
    company=['.'.join(company[i]) for i in range(0,len(company))]
    #keyword
    key_list=[key]*len(company)
    sector=[sector]*len(company)
    return company, sector, key_list, url, research, development, innovation, design, extra_info

if my_file.exists():
    text=open(fname, 'r+',  encoding='utf-8')
    list_with_text = text.read().splitlines()
    columns=['Company','Sector','Keyword','url','Design','Development','Innovation','Research', 'Extra']
    df=pd.DataFrame(columns=columns)
    company, sector, key_list, url, research, development, innovation, design, extra_info = create_lst(fname, key, s)
else:
    company, sector, key_list, url, research, development, innovation, design, extra_info=  ([] for i in range(0,9))

#use the second file .txt (if there is one)

pathname = os.path.dirname(sys.argv[0]) 
path_name=os.path.abspath(pathname)
fname=os.path.join(path_name+ '/'+s+'_freq2.txt' )
key='keyword_2'
my_file = Path(fname)
if my_file.exists():
    text=open(fname, 'r+',  encoding='utf-8')    
    list_with_text = text.read().splitlines()
    company2, sector2, key_list2, url2, research2, development2, innovation2, design2, extra_info2 = create_lst(fname, key, s)

    company+=company2
    sector+=sector2
    key_list+=key_list2
    url+=url2
    research+=research2
    development+=development2
    innovation+=innovation2
    design+=design2
    extra_info+=extra_info2


# Construct dataframe
df['Company']=company
df['Sector']=sector
df['Keyword']=key_list
df['url']=url
df['Design']=design
df['Development']=development
df['Innovation']=innovation  
df['Research']=research 
df['Extra']=extra_info


# write to output
path=os.path.join(path_name,'Frequencies')
if not os.path.exists(path): os.makedirs(path)
fname_freq=os.path.join(path, s+'url_frequencies_07_04.csv')
df.to_csv(fname_freq, index=False)

