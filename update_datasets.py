import PETS

LOST_CATS_WEBPAGE_URL = "https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1"
LOST_DOGS_WEBPAGE_URL = "https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_DOG&PAGE=1"
LOST_OTHERS_WEBPAGE_URL = "https://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_OO&PAGE=1"
ADOPTABLE_CATS_WEBPAGE_URL = "https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&view=sysadm.v_sncr&bgcolor=white&text=black&link=blue&alink=purple&vlink=purple&fontface=arial&fontsize=10&col_hdr_bg=silver&col_hdr_fg=black&col_bg=white&col_fg=black&SBG=silver&miles=200&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1"
ADOPTABLE_DOGS_WEBPAGE_URL = "https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&view=sysadm.v_sncr&bgcolor=white&text=black&link=blue&alink=purple&vlink=purple&fontface=arial&fontsize=10&col_hdr_bg=silver&col_hdr_fg=black&col_bg=white&col_fg=black&SBG=silver&miles=200&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_DOG&PAGE=1"
ADOPTABLE_OTHERS_WEBPAGE_URL = "https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&view=sysadm.v_sncr&bgcolor=white&text=black&link=blue&alink=purple&vlink=purple&fontface=arial&fontsize=10&col_hdr_bg=silver&col_hdr_fg=black&col_bg=white&col_fg=black&SBG=silver&miles=200&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_OO&PAGE=1"

PET_MAP = {
    "cats": [LOST_CATS_WEBPAGE_URL, ADOPTABLE_CATS_WEBPAGE_URL],
    "dogs": [LOST_DOGS_WEBPAGE_URL, ADOPTABLE_DOGS_WEBPAGE_URL],
    "others": [LOST_OTHERS_WEBPAGE_URL, ADOPTABLE_OTHERS_WEBPAGE_URL],
}

for PET, URLS in PET_MAP.items():
    LOST_DATA_PATH = "Datasets/" + f"lost_{PET}_data.csv"
    ADOPTABLE_DATA_PATH = "Datasets/" + f"adoptable_{PET}_data.csv"
    LOST_URL = URLS[0]
    ADOPTABLE_URL = URLS[1]
    PETS.PETS(URL=LOST_URL).UpdateData(DATA_PATH=LOST_DATA_PATH)
    PETS.PETS(URL=ADOPTABLE_URL).UpdateData(DATA_PATH=ADOPTABLE_DATA_PATH)
