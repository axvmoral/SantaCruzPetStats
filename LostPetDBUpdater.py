import pandas as pd
from HelperFunctions import *
from datetime import datetime
import sqlite3
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def UpdateLostPetDB(pet: str, db: str, table) -> None:
    lst = datetime.now()
    print(f'Commencing {table} Table Update...')
    print('Retrieving Web Data...')
    MATCHES = get_matches(type=pet)
    url = f'https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows={MATCHES}&imght=120&imgres=Detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_{pet}&PAGE=1'
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
    TODAY = datetime.today().strftime('%Y-%m-%d')
    df['FirstWeb'] = TODAY
    df['LastDate'] = None
    print('Web Data Succesfully Retrieved')
    print(f'Updating {table}...')
    VALUES = '(?' + ',?' * (len(df.columns) - 2)  + ')'
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''CREATE TABLE
                NewWebData(ID PRIMARY KEY, Name TEXT, Gender TEXT,
                Color TEXT, Breed TEXT, Age DECIMAL, Weight DECIMAL, Located TEXT,
                EnterDate TEXT, Comment TEXT, Polarity REAL, InGroup INTEGER,
                Treated INTEGER, RawGender INTEGER, FirstWeb TEXT, LastDate TEXT)
                ''')
    cur.executemany(f'INSERT INTO NewWebData VALUES{VALUES}', (row[1] for row in df.iloc[:,1:].iterrows()))
    cur.execute(f'SELECT {table}.ID FROM {table} LEFT JOIN NewWebData ON {table}.ID = NewWebData.ID WHERE NewWebData.ID IS NULL AND {table}.LastDate IS NULL')
    gone = cur.fetchall()
    print(f'{len(gone)} {pet.lower()}(s) gone from website')
    cur.executemany(f'UPDATE {table} SET LastDate = "{TODAY}" WHERE ID = ?', gone)
    cur.execute(f'SELECT NewWebData.* FROM NewWebData LEFT JOIN {table} ON NewWebData.ID = {table}.ID WHERE {table}.ID IS NULL')
    new = cur.fetchall()
    print(f'{len(new)} new {pet.lower()}(s) on website')
    cur.executemany(f'INSERT INTO {table} VALUES{VALUES}', new)
    cur.execute('DROP TABLE NewWebData')
    con.commit()
    con.close()
    print(f'{table} Succesfully Updated')
    let = datetime.now()
    print(f'Time Elapsed: {let - lst}\n')
    return None

if __name__ == '__main__':
    gst = datetime.now()
    print('Commencing Pets Data Base Update...\n')
    UpdateLostPetDB(pet='CAT', db='data/Pets.db', table='LostCats')
    UpdateLostPetDB(pet='DOG', db='data/Pets.db', table='LostDogs')
    get = datetime.now()
    print('Pets Data Base Succesfully Updated')
    print(f'Total Time Elapsed: {get - gst}')
