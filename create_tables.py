""" Module to create tables. """

__author__ = "Axel V. Morales Sanchez"

import sqlite3

DATABASE_LOCATION = "C:/Users/axvmo/OneDrive/Documents/GitHub/SantaCruzPetStats/santaCruzPets.db"

con = sqlite3.connect(DATABASE_LOCATION)
cur = con.cursor()

with open("raw_links") as file:
    for line in file:
        tableName = line[: line.find(" ") + 1]
        createTable = f"""
            CREATE TABLE {tableName} (
	        id CHAR(7) NOT NULL,
	        name VARCHAR(30),
	        gender VARCHAR(20),
	        color VARCHAR(20),
	        breed VARCHAR(30),
	        age VARCHAR(20),
	        weight VARCHAR(20),
	        located VARCHAR(20),
            entranceDate date,
            exitDate date,
            PRIMARY KEY (id)
            )
        """
        createIndex = f"""
            CREATE INDEX "{tableName}_id"
            ON {tableName} (id)
        """
        cur.execute(createTable)
        cur.execute(createIndex)
con.commit()
con.close()
