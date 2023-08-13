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
print('Retrieving Web Data...')
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
today = datetime.today().strftime('%Y-%m-%d')
df['FirstWeb'] = today
df['LastDate'] = None
print('Web Data Succesfully Retrieved')
print('Updating Data Base...')
VALUES = '(?' + ',?' * (len(df.columns) - 2)  + ')'
con = sqlite3.connect('data/LostCatDataBase.db')
cur = con.cursor()
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS
    NewWebData(ID PRIMARY KEY, Name TEXT, Gender TEXT,
    Color TEXT, Breed TEXT, Age DECIMAL, Weight DECIMAL, Located TEXT,
    EnterDate TEXT, Comment TEXT, Polarity REAL, InGroup INTEGER,
    Treated INTEGER, RawGender INTEGER, FirstWeb TEXT, LastDate TEXT)
    '''
    )
cur.executemany(f'INSERT INTO NewWebData VALUES{VALUES}', (row[1] for row in df.iloc[:,1:].iterrows()))
cur.execute('SELECT WebData.ID FROM WebData LEFT JOIN NewWebData ON WebData.ID = NewWebData.ID WHERE NewWebData.ID IS NULL AND WebData.LastDate IS NULL')
cur.executemany(f'UPDATE WebData SET LastDate = "{today}" WHERE ID = ?', cur.fetchall())
cur.executemany(f'INSERT OR IGNORE INTO WebData VALUES{VALUES}', (row[1] for row in df.iloc[:,1:].iterrows()))
cur.execute('DROP TABLE NewWebData')
con.commit()
con.close()
print('Data Base Succesfully Updated')
et = datetime.now()
print(f'Time Elapsed: {et - st}')
