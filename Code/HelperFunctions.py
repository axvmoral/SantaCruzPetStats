import re
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
from datetime import datetime


group_words = {
    'litter', 'kittens', 'cats', 'kitties', 'litterbox',
    'set', 'cuties', 'group', 'newborns', 'pair', 'they',
    'them', 'these', 'their', 'they\'re', 'companion'
}

def age_getter(age: str) -> float:
    if age == 'Age Unknown':
        return None
    pattern = '([0-9]+) day[s]*\s*[old]*|([0-9]+) week[s]*\s*[old]*|([0-9]+) month[s]*\s*[old]*|([0-9]+) year[s]*\s*[old]*,*\s*([0-9]*)\s*[months old]*'
    re_list = [float(x) if x else 0 for x in re.findall(pattern, age)[0]]
    return re_list[0] / 30 + re_list[1] / 4 + re_list[2] + re_list[3] / 12 + re_list[4]

def group_det(text: str, degree: int) -> bool:
    if not text:
        return False
    else:
        key_word_count = 0
        for word in [word.strip('.?!:; ').lower() for word in text.translate(text.maketrans('.!?:;', '     ')).split()]:
            if word in group_words:
                key_word_count += 1
            if key_word_count == degree:
                return True
        return False

def get_matches(type: str) -> int:
    if type == 'lost.cat':
        url = 'http://petharbor.com/results.asp?searchtype=LOST&start=4&friends=1&samaritans=1&nosuccess=0&rows=10&imght=120&imgres=Detail&tWidth=200&view=sysadm.v_sncr&nobreedreq=1&bgcolor=ffffff&text=000000&fontface=arial&fontsize=10&col_hdr_bg=c0c0c0&SBG=c0c0c0&miles=20&shelterlist=%27SNCR%27,%27SNCR1%27&atype=&where=type_CAT&PAGE=1'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        return int(re.findall('We found ([0-9]+) matches', soup.text)[0])

def visit_links(links: list) -> list[list]:
    EnterDate, Comment, Polarity, InGroup = [], [], [], []
    for link in links:
        res = requests.get(link)
        soup = BeautifulSoup(res.content, 'html.parser')
        date = re.findall('I have been at the shelter since (.+?)[.]', soup.find(attrs={'class': 'DetailDesc'}).text)[0]
        EnterDate.append(
            datetime.strptime(date, r'%b %d, %Y').strftime('%Y-%m-%d')
        )
        comment_list = re.findall(
            'Shelter Staff made the following comments about this animal:(.+)',
            soup.findAll('table')[1].text.strip()
        )
        comment = comment_list[0] if comment_list else None
        Comment.append(comment)
        InGroup.append(1 if group_det(comment, degree=3) else (0 if comment else None))
        Polarity.append(TextBlob(comment).sentiment.polarity if comment else None)
    return [EnterDate, Comment, Polarity, InGroup]

def get_treatment(gender: str) -> int:
    if gender.startswith('U'):
        return None
    elif gender.startswith('M') or gender.startswith('F') and gender.endswith('SPAYED') or gender.endswith('NEUTERED'):
        return 1
    else:
        return 0

def get_raw_gender(gender: str) -> int:
    genders = re.findall('(FEMALE)|(MALE)', gender)
    return None if not genders else (0 if genders[0][0] else 1)
