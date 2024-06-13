""" Module for updating database. """

import pandas as pd
import sqlite3
from datetime import datetime

DATABASE_LOCATION = "C:/Users/axvmo/OneDrive/Documents/GitHub/SantaCruzPetStats/santaCruzPets.db"

con = sqlite3.connect(DATABASE_LOCATION)
cur = con.cursor()
currentDate = datetime.today().strftime("%Y-%m-%d")

createTempTable = """
CREATE TEMPORARY TABLE pulledResults (
	id CHAR(7),
	name VARCHAR(30),
	gender VARCHAR(20),
	color VARCHAR(20),
	breed VARCHAR(30),
	age VARCHAR(20),
	weight VARCHAR(20),
	located VARCHAR(20)
)
"""
dropTempTable = "DROP TABLE pulledResults"
insertIntoTempTable = "INSERT INTO pulledResults VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

with open("scraping_links") as file:
    for line in file:
        spaceIndex = line.find(" ")
        tableName = line[:spaceIndex]
        url = line[spaceIndex + 1 :]
        resultsTable = pd.read_html(url, attrs={"class": "ResultsTable"}, header=0)[0].drop(
            columns="Picture"
        )
        cur.execute(createTempTable)
        cur.executemany(
            insertIntoTempTable, resultsTable.drop(0).itertuples(index=False, name=None)
        )
        updateDatabase = f"""
            UPDATE {tableName}
            SET exitDate = '{currentDate}'
            WHERE exitDate IS NULL AND id NOT IN (SELECT id FROM pulledResults)
        """
        cur.execute(updateDatabase)
        insertPulled = f"""
            INSERT INTO {tableName} (id, name, gender, color, breed, age, weight, located, entranceDate, exitDate)
            SELECT pulled.*,
            '{currentDate}' AS entranceDate,
            NULL AS exitDate
            FROM pulledResults AS pulled
            LEFT JOIN {tableName} AS current
            ON pulled.id = current.id
            WHERE current.id IS NULL
        """
        cur.execute(insertPulled)
        cur.execute(dropTempTable)
con.commit()
con.close()
