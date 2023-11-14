import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pandas as pd
from pandas import DataFrame
import os


class PETS:
    def __init__(self, URL) -> None:
        TEMPORARY_SOUP = BeautifulSoup(requests.get(URL).content, "html.parser")
        MATCHES = re.search(r"We found (\d+) matches", TEMPORARY_SOUP.text).group(1)
        NEW_URL = re.sub(r"rows=(\d+)", f"rows={MATCHES}", URL)
        URL_ROOT = URL[: URL.find("/") + 1]
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
        self.DATAFRAME = pd.DataFrame(data).rename({"Picture": "InfoLink"}).set_index(keys="ID")
        return None

    def PrepareData(self, data: DataFrame) -> None:
        data.Name = data.Name.map(lambda x: x.strip("*").lower(), na_action="ignore")
        data.Color = data.Color.map(lambda x: x.strip().lower(), na_action="ignore")
        data.Breed = data.Breed.map(lambda x: x.strip().lower(), na_action="ignore")
        data["Treated"] = data.Gender.str.contains(r"neutered|spayed", case=False)
        AGE_PATTERN = r"(\d+).*?(?=year)|(\d+).*?(?=month)|(\d+).*?(?=week)|(\d+).*?(?=day)"
        data["MonthAge"] = (
            data.Age.str.extract(AGE_PATTERN, flags=re.IGNORECASE)
            .apply(pd.to_numeric)
            .assign(
                Year=lambda x: x[0] / 12,
                Month=lambda x: x[1],
                Week=lambda x: x[2] * 4,
                Day=lambda x: x[3] * 31,
            )[["Year", "Month", "Week", "Day"]]
            .sum(axis=1)
        )
        data.Weight = data.Weight.map(lambda x: float(x.lower().strip("lbs")), na_action="ignore")
        data.Gender = data.Gender.str.contains(r"male", case=False)
        return data

    def UpdateData(self, EXISTING_DATA_PATH: str) -> None:
        EXISTS = os.path.exists(EXISTING_DATA_PATH)
        if EXISTS:
            EXISTING_DATA = pd.read_csv(EXISTING_DATA_PATH, index_col="ID")
            INTERSECTING_INDEX = EXISTING_DATA.index.intersection(self.DATAFRAME.index)
            NEW_DATA = self.PrepareData(self.DATAFRAME[INTERSECTING_INDEX])
        else:
            NEW_DATA = self.DATAFRAME
        NEW_DATA.to_csv(EXISTING_DATA_PATH, mode="a", header=EXISTS)
        return None


if __name__ == "__main__":
    URL = "https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=139&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1"
    pets = PETS(URL)
    d = pets.PrepareData(pets.DATAFRAME)
