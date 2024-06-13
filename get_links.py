""" Module for computing links with maximum row argument. """

__author__ = "Axel V. Morales Sanchez, axvmoral@ucsc.edu"

import requests
from bs4 import BeautifulSoup
import re

with open("scraping_links", "w") as file1:
    with open("raw_links") as file2:
        for line in file2:
            spaceIndex = line.find(" ")
            tableName = line[: spaceIndex + 1]
            url = line[spaceIndex + 1 :]
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            matches = re.search(r"\d+", soup.find("center").text).group(0)
            scrapingLink = re.sub("rows=\d+", f"rows={matches}", url)
            file1.write(tableName + scrapingLink)
