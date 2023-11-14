import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pandas as pd
from pandas import DataFrame
import os
from datetime import datetime


class PETS:
    def __init__(self, URL) -> None:
        TEMPORARY_SOUP = BeautifulSoup(requests.get(URL).content, "html.parser")
        MATCHES = re.search(r"We found (\d+) matches", TEMPORARY_SOUP.text).group(1)
        NEW_URL = re.sub(r"rows=(\d+)", f"rows={MATCHES}", URL)
        URL_ROOT = URL[: URL.rfind("/") + 1]
        SOUP = BeautifulSoup(requests.get(NEW_URL).content, "html.parser")
        TABLE = SOUP.find(attrs={"class": "ResultsTable"})
        ROWS = TABLE.find_all("tr")
        HEADERS = [ENTRY.text.strip() for ENTRY in ROWS[0].find_all("td")]
        data = defaultdict(list)
        for ROW in ROWS[1:]:
            for j, ENTRY in enumerate(ROW.find_all("td")):
                if j == 0:
                    data[HEADERS[j]].append(URL_ROOT + ENTRY.a.get("href"))
                    data["ImageLink"].append(URL_ROOT + ENTRY.img.get("src"))
                elif re.search(r"unknown", ENTRY.text, re.IGNORECASE):
                    data[HEADERS[j]].append(None)
                else:
                    data[HEADERS[j]].append(ENTRY.text)
        self.DATAFRAME = (
            pd.DataFrame(data).rename(columns={"Picture": "InfoLink"}).set_index(keys="ID")
        )
        return None

    def VisitLink(self, LINK: str) -> tuple[str]:
        LINK_SOUP = BeautifulSoup(requests.get(LINK).content, "html.parser")
        DETAIL_TABLES = LINK_SOUP.find_all("table", attrs={"class": "DetailTable"})
        DESCRIPTION_TABLE = DETAIL_TABLES[0]
        SHELTER_SINCE_SEARCH = re.search(
            r"I have been at the shelter since(.+?)[.]", DESCRIPTION_TABLE.text, flags=re.IGNORECASE
        )
        SHELTER_SINCE = (
            pd.to_datetime(SHELTER_SINCE_SEARCH.group(1)).date()
            if SHELTER_SINCE_SEARCH is not None
            else None
        )
        COMMENT_TABLE = DETAIL_TABLES[1]
        COMMENT_SEARCH = re.search(r":(.+)", COMMENT_TABLE.text)
        COMMENT = COMMENT_SEARCH.group(1) if COMMENT_SEARCH is not None else None
        return (SHELTER_SINCE, COMMENT)

    def PrepareData(self, DATA: DataFrame) -> None:
        data = DATA.copy()
        data.Name = data.Name.map(lambda x: x.strip("*").lower(), na_action="ignore")
        data.Color = data.Color.map(lambda x: x.strip().lower(), na_action="ignore")
        data.Breed = data.Breed.map(lambda x: x.strip().lower(), na_action="ignore")
        data.Weight = data.Weight.map(lambda x: float(x.lower().strip("lbs")), na_action="ignore")
        data["Treated"] = data.Gender.str.contains(r"neutered|spayed", case=False)
        data["FemaleGender"] = data.Gender.str.contains(r"female", case=False)
        for TIME in ["Year", "Month", "Week", "Day"]:
            data[f"Age{TIME}"] = data.Age.str.extract(
                f"(\d+).*?(?={TIME})", flags=re.IGNORECASE, expand=False
            )
        link_info = defaultdict(list)
        for LINK in data.InfoLink:
            SHELTER_SINCE, COMMENT = self.VisitLink(LINK)
            link_info["ShelterSince"].append(SHELTER_SINCE)
            link_info["Comment"].append(COMMENT)
        data["ShelterSince"] = link_info["ShelterSince"]
        data["Comment"] = link_info["Comment"]
        data["ScrapedOn"] = datetime.today().date()
        return data

    def UpdateData(self, DATA_PATH: str) -> None:
        EXISTS = os.path.exists(DATA_PATH)
        if EXISTS:
            EXISTING_DATA = pd.read_csv(DATA_PATH, usecols=["ID"], index_col="ID")
            DIFFERENCE_INDEX = self.DATAFRAME.index.difference(EXISTING_DATA.index)
            NEW_DATA = self.PrepareData(self.DATAFRAME.loc[DIFFERENCE_INDEX])
        else:
            DIRNAME = os.path.dirname(DATA_PATH)
            if not os.path.exists(DIRNAME):
                os.mkdir(DIRNAME)
            NEW_DATA = self.PrepareData(self.DATAFRAME)
        NEW_DATA.to_csv(DATA_PATH, mode="a", header=not EXISTS)
        return None


if __name__ == "__main__":
    URL = "https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=139&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1"
    pets = PETS(URL)
    pets.UpdateData("Datasets/lost_cats.csv")
    df = pd.read_csv("Datasets/lost_cats.csv")
