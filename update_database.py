from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from helper_functions import get_line_info

db = "pets.db"
update_info = [
    ("https://24petconnect.com/SantaCruzStray?at=DOG", "lost_dogs"),
    ("https://24petconnect.com/SantaCruzStray?at=CAT", "lost_cats"),
    ("https://24petconnect.com/SantaCruzStray?at=OTHER", "lost_others"),
    ("https://24petconnect.com/SantaCruzAdoptable?at=DOG", "adoptable_dogs"),
    ("https://24petconnect.com/SantaCruzAdoptable?at=CAT", "adoptable_cats"),
    ("https://24petconnect.com/SantaCruzAdoptable?at=OTHER", "adoptable_others"),
]
indiv_page_info = [
    ("located_at", "line_LocatedAt details", "text_LocatedAt details"),
    ("date_found", "line_Date details", "text_Date details"),
    ("description", "line_Description details", "text_Description details"),
    ("age", "line_Age details", "text_Age details"),
    ("more_info", "line_MoreInfo details", "text_MoreInfo details"),
    ("location_found", "line_LocationFound details", "text_LocationFound details"),
]
main_page_info = [
    ("name", "line_Name", "text_Name results"),
    ("gender", "line_Gender", "text_Gender results"),
    ("animal_type", "line_AnimalType", "text_AnimalType results"),
    ("days_since_found", "line_DaysSinceFound", "text_DaysSinceFound results"),
    ("breed", "line_Breed", "text_Breed results"),
    ("weight", "line_Weight", "text_Weight results"),
    ("lost_or_found", "line_LostorFound", "text_LostorFound results"),
    ("location", "line_Location", "text_Location results"),
]
cols = ["id"] + [x[0] for x in main_page_info + indiv_page_info] + ["date_scraped"]
col_statement = ", ".join(cols)
values_statement = "?, " * (len(cols) - 1) + "?"
today = datetime.today().date().isoformat()

driver = webdriver.Chrome()

for url, table in update_info:
    driver.get(url)
    x = len(driver.find_elements(By.CLASS_NAME, "page-link")) - 2

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        CREATE TEMP TABLE "temp" (
            "id"	TEXT NOT NULL UNIQUE,
            PRIMARY KEY("id")
        );
        """
    )

    for i in range(x):
        for result in driver.find_elements(By.CLASS_NAME, "gridResult"):
            ID = result.get_attribute("id")
            ID = ID[ID.find("_") + 1 :]
            cur.execute("INSERT INTO temp (id) VALUES (?)", (ID,))
            cur.execute(f"SELECT id FROM {table} WHERE id = '{ID}'")
            res = cur.fetchone()
            if res is None:
                row = []
                row.append(ID)
                soup = BeautifulSoup(result.get_attribute("innerHTML"), "html.parser")
                for col, line_indicator, text_indicator in main_page_info:
                    row.append(get_line_info(soup, line_indicator, text_indicator))
                result.click()
                detail_box = driver.find_element(By.CLASS_NAME, "animalDetailsBox")
                soup = BeautifulSoup(
                    detail_box.get_attribute("innerHTML"), "html.parser"
                )
                for col, line_indicator, text_indicator in indiv_page_info:
                    row.append(get_line_info(soup, line_indicator, text_indicator))
                row.append(today)
                cur.execute(
                    f"""
                    INSERT INTO
                            {table} ({col_statement})
                    VALUES
                            ({values_statement})
                    """,
                    row,
                )
                driver.back()
        next_page = driver.find_elements(By.CLASS_NAME, "page-link")[-1]
        if i + 1 < x:
            next_page.click()

    cur.executescript(
        f"""
        UPDATE 
            {table}
        SET 
            date_last_website = '{today}'
        WHERE
            id NOT IN (SELECT id FROM temp)
        ;

        DROP TABLE temp
        ;
        """
    )

driver.close()
con.commit()
con.close()
