from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
from pandas import DataFrame
import requests
import sqlite3
from datetime import date


def get_raw_data(url: str) -> DataFrame:
    """
    Scrapes lowered and stripped data from the main data table
    in the Santa Cruz County Pet Shelter adopt or lost pet website
    indicated by the url parameter.

    :param url: the url of the adopt or lost website
    :return: a DataFrame representation of the main data table
    """
    with webdriver.Chrome() as driver:
        driver.get(url)
        html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    matches = re.search(r"We found (?P<matches>\d+) matches", soup.find("center").text)[
        "matches"
    ]
    url = re.sub(r"rows=\d+", f"rows={matches}", url)
    url_root = url[: url.rfind("/") + 1]
    df = pd.read_html(url, attrs={"class": "ResultsTable"}, extract_links="all")[0]
    df.columns = [x[0].lower().strip() for x in df.iloc[0]]
    df.drop(index=0, inplace=True)
    urls = df["picture"].map(lambda x: url_root + x[1])
    df = df.drop(columns="picture").apply(lambda x: [y[0].lower().strip() for y in x])
    df["url"] = urls
    return df


def get_profile_info(
    url: str,
) -> tuple[str | None, str | None]:
    """
    Scrapes the individual website of a Santa Cruz County Animal
    Shelter pet for the date that pet has been at the shelter (shelter 
    since date) and the comment left by shelter staff for that pet if any.

    :param url: the url of an individual pet's website
    :return: a tuple containing the shelter since date and the shelter
    staff comment
    """
    shelter_since = None
    comment = None
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    detail_tables = soup.find_all("table", attrs={"class": "DetailTable"})
    if detail_tables:
        shelter_since_match = re.search(
            r"I have been at the shelter since\s*(?P<shelter_since>.+?)[.]",
            detail_tables[0].text,
        )
        if shelter_since_match is not None:
            shelter_since = shelter_since_match["shelter_since"]
    if len(detail_tables) == 3:
        comment_match = re.search(
            r"Shelter Staff made the following comments about this animal:(?P<comment>.+)",
            detail_tables[1].text,
        )
        if comment_match is not None:
            comment = comment_match["comment"]
    return (shelter_since, comment)

def get_day_age(age_string: str) -> int | None:
    """
    Determines the day age of a pet from a description of how
    old it is.

    :param age_string: a string description of how old the pet is
    in the form of for example "1 year, 2 months, 3 week, 4 days".
    :return: an integer representation of the day age of the pet
    """
    conversions = {"year": 365, "month": 30, "week": 7, "day": 1}
    age = 0
    for time, converstion in conversions.items():
        age_match = re.search(f"(?P<age>\d+)\s*{time}s*", age_string)
        if age_match is not None:
            age += int(age_match["age"]) * converstion
    return age if age > 0 else None

def update_database(lost_url: str, adoptable_url: str, database_path: str, table: str) -> None:
    """
    Updates the database with data of a given pet group.

    :param lost_url: the url of the lost website for that pet group
    :param adoptable_url: the url of the adoption website for that pet group
    :param database_path: the path of the database
    :param table: the table name in the database 
    """
    lost = get_raw_data(lost_url)
    adoptable = get_raw_data(adoptable_url)

    a = pd.merge(lost, adoptable["id"], on="id", how="left", indicator=True)
    b = pd.merge(lost["id"], adoptable, on="id", how="right", indicator=True).loc[
        lambda x: x["_merge"] == "right_only"
    ]
    current = pd.concat([a, b], ignore_index=True)

    shelter_since_dates = []
    comments = []
    for url in current["url"]:
        shelter_since, comment = get_profile_info(url)
        shelter_since_dates.append(shelter_since)
        comments.append(comment)

    genders = []
    steralizations = []
    for gender_str in current["gender"]:
        gender = None
        steralized = None
        info = re.findall(r"(f*e*male|spayed|neutered)", gender_str)
        if info:
            gender = info[0]
            if len(info) > 1:
                steralized = True
            else:
                steralized = False
        genders.append(gender)
        steralizations.append(steralized)

    current["gender_only"] = genders
    current["steralized"] = steralizations
    current["shelter_since"] = shelter_since_dates
    current["commment"] = comments
    current["date"] = date.today().strftime("%m/%d/%Y")
    current["day_age"] = current["age"].map(get_day_age)
    current["lb_weight"] = current["weight"].str.extract("(\d+[.]\d+)").astype(float)
    current.drop(columns=["gender", "age", "weight"], inplace=True)

    con = sqlite3.connect(database_path)
    cur = con.cursor()

    cur.executescript(open("sql/setup.sql").read())

    cur.execute(
        """
        CREATE TEMP TABLE "current" (
            "id"	TEXT,
            "name"	TEXT,
            "date"	TEXT,
            "gender"	TEXT,
            "color"	TEXT,
            "breed"	TEXT,
            "day_age"	INTEGER,
            "lb_weight"	REAL,
            "steralized"	INTEGER,
            "located"	TEXT,
            "shelter_since"	TEXT,
            "comment"	TEXT,
            "url"	TEXT,
            "_merge"	TEXT
        );
        """
    )

    values = f"({', '.join(['?'] * len(current.columns))})"
    cur.executemany(
        f"""
        INSERT INTO 
            current
            (
                id,
                name,
                color,
                breed,
                located,
                url,
                _merge,
                gender,
                steralized,
                shelter_since,
                comment,
                date,
                day_age,
                lb_weight
            )
        VALUES {values}
        """,
        current.itertuples(index=False, name=None),
    )

    cur.executescript(
        f"""
        INSERT INTO
            {table}
            (
                id,
                name,
                gender,
                color,
                breed,
                day_age_when_scraped,
                shelter_since,
                date_first_lost_website,
                date_first_adopt_website,
                comment,
                url
            )
        SELECT
            id,
            name,
            gender,
            color,
            breed,
            day_age,
            shelter_since,
            CASE 
                WHEN 
                    _merge = 'left_only' OR _merge = 'both'
                THEN
                    "date"
                ELSE
                    NULL
            END date_first_lost_website,
            CASE 
                WHEN 
                    _merge = 'right_only' OR _merge = 'both'
                THEN
                    "date"
                ELSE
                    NULL
            END date_first_adopt_website,
            comment,
            url
        FROM current
        WHERE true
        ON CONFLICT (id) DO UPDATE SET
            name = excluded.name,
            gender = excluded.gender,
            color = excluded.color,
            breed = excluded.breed,
            day_age_when_scraped = CASE WHEN day_age_when_scraped IS NULL THEN excluded.day_age_when_scraped ELSE day_age_when_scraped END,
            shelter_since = excluded.shelter_since,
            date_first_lost_website = CASE WHEN date_first_lost_website IS NULL THEN excluded.date_first_lost_website ELSE date_first_lost_website END,
            date_first_adopt_website = CASE WHEN date_first_adopt_website IS NULL THEN excluded.date_first_adopt_website ELSE date_first_adopt_website END,
            comment = excluded.comment
        ;

        INSERT OR IGNORE INTO
            {table}_time
        SELECT
            id,
            "date",
            lb_weight,
            located,
            steralized
        FROM
            current
        ;

        DROP TABLE current;
        """
    )

    con.commit()
