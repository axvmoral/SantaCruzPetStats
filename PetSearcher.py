from bs4 import BeautifulSoup
import requests
from HelperFunctions import get_matches

pet = "CAT"
MATCHES = get_matches(type=pet)
url = f"https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows={MATCHES}&imght=120&imgres=Detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_{pet}&PAGE=1"


def get_img_urls(url: str) -> list:
    img_urls = []
    soup = BeautifulSoup(requests.get(url=url).content, "html.parser")
    for img in soup.find("table", {"class": "ResultsTable"}).find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        else:
            img_urls.append(url[url.rfind("/")] + img_url)
