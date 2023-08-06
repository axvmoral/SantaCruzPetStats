import re
from webbrowser import get
import requests
from bs4 import BeautifulSoup
import pandas as pd
from HelperFunctions import *
from datetime import datetime
from textblob import TextBlob
import sqlite3

st = datetime.now()
matches = get_matches(type='lost.cat')
url = f'https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows={matches}&imght=120&imgres=Detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1'
df = pd.read_html(
    io=url,
    attrs={'class': 'ResultsTable'},
    extract_links='all',
    skiprows=1,
    converters={
        0: lambda x: 'https://petharbor.com/' + x[1], #InfoLink
        1: lambda x: x[0], #ID
        2: lambda x: x[0].strip('*').upper(), #Name
        3: lambda x: x[0].upper(), #Gender
        4: lambda x: x[0].upper(), #Color
        5: lambda x: x[0].upper(), #Breed
        6: lambda x: age_getter(x[0]), #Age
        7: lambda x: None if x[0].startswith('U') else float(x[0].strip('Lbs')), #Weight
        8: lambda x: x[0] #Located
    }
)[0]
LinkResults = visit_links(df[0])
for i in range(len(LinkResults)):
    df[i + len(df)] = LinkResults[i]
df.columns = ['InfoLink', 'ID', 'Name', 'Gender', 'Color', 'Breed', 'Age', 'Weight', 'Located',
              'EnterDate', 'Comment', 'Polarity', 'InGroup']
df['Treated'] = df.apply(lambda x: get_treatment(x['Gender']), axis=1)
df['RawGender'] = df.apply(lambda x: get_raw_gender(x['Gender']), axis=1)
print('Web Data Succesfully Retrieved')
con = sqlite3.connect('data/LostCatDataBase.db')
cur = con.cursor()
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS
    WebData(ID PRIMARY KEY, InfoLink TEXT, Name TEXT, Gender TEXT,
    Color TEXT, Breed TEXT, Age DECIMAL, Weight DECIMAL, Located TEXT,
    EnterDate TEXT, Comment TEXT, Polarity REAL, InGroup INTEGER,
    Treated INTEGER, RawGender INTEGER, FirstWeb TEXT)
    '''
    )
NewWebDataIDs = []
for i in range(len(df)):
    cur.execute('SELECT EXISTS(SELECT 1 FROM WebData WHERE ID = ?)', (df['ID'][i], ))
    if cur.fetchone():
        NewWebDataIDs.append(df['ID'][i])
NewWebData = pd.DataFrame(data={'ID': NewWebDataIDs}).merge(df, how='inner', on='ID')
NewWebData['FirstWeb'] = datetime.today().strftime('%Y-%m-%d')
for i in range(len(NewWebData)):
    cur.execute(
        '''
        INSERT OR IGNORE INTO WebData VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', NewWebData.iloc[i,:]
    )
con.commit()
con.close()
print('Data Base Succesfully Updated')
et = datetime.now()
print(f'Time Elapsed: {et - st}')
