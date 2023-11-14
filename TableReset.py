import sqlite3

con = sqlite3.connect("data/Pets.db")
cur = con.cursor()
# cur.execute('DROP TABLE WebData')
# cur.execute('DROP TABLE NewWebData')
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS
    LostDogs(ID PRIMARY KEY, Name TEXT, Gender TEXT,
    Color TEXT, Breed TEXT, Age DECIMAL, Weight DECIMAL, Located TEXT,
    EnterDate TEXT, Comment TEXT, Polarity REAL, InGroup INTEGER,
    Treated INTEGER, RawGender INTEGER, FirstWeb TEXT, LastDate TEXT)
    """
)
# con.commit()
# con.close()
print("Tables Reset")
