from bs4 import BeautifulSoup


def get_line_info(
    soup: BeautifulSoup, line_indicator: str, text_indicator: str
) -> str | None:
    line = soup.find("div", attrs={"class": line_indicator})
    if line is not None:
        text = line.find("span", attrs={"class": text_indicator})
        if text is not None:
            return text.text
        else:
            return text
    else:
        return line
