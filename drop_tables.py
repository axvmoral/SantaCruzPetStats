""" Module to drop tables. """

__author__ = "Axel V. Morales Sanchez"

import sqlite3

DATABASE_LOCATION = "C:/Users/axvmo/OneDrive/Documents/GitHub/SantaCruzPetStats/santaCruzPets.db"

con = sqlite3.connect(DATABASE_LOCATION)
cur = con.cursor()

with open("raw_links") as file:
    for line in file:
        tableName = line[: line.find(" ") + 1]
        dropTable = f"DROP TABLE {tableName}"
        cur.execute(dropTable)
con.commit()
