import json
import re
from datetime import datetime
from typing import Optional

from jivago.lang.stream import Stream

from ohdieux.util.safe_dict import SafeDict

MONTHS = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12
}

ABBR_MONTHS = {
    "jan.": 1,
    "fév.": 2,
    "mar.": 3,
    "avr.": 4,
    "mai": 5,
    "juin": 6,
    "juil": 7,
    "août": 8,
    "sept.": 9,
    "oct.": 10,
    "nov.": 11,
    "déc.": 12
}


def parse_fr_date(formatted: str) -> datetime:
    day, month, year = formatted.lower().split(" ")
    try:
        return datetime(int(year), MONTHS[month], int(day.rstrip("er")))
    except:
        pass
    return datetime(int(year), ABBR_MONTHS[month], int(day.rstrip("er")))


def infer_fr_date(item: dict) -> datetime:
    x = SafeDict(item)
    candidates = [
        x["media2"]["details"].value(),
        x["title"].value(),
        x["description"]["title"].value(),
        x["header"]["media2"]["title"].value(),
    ]
    try:
        return Stream(candidates).map(extract_tentative_date).filter(lambda x: x is not None).max()
    except:
        return datetime(year=2000, month=1, day=1)


def extract_tentative_date(text: str) -> Optional[datetime]:
    for month in Stream(MONTHS.keys(), ABBR_MONTHS.keys()):
        try:
            match = re.search(r"\d{1,2}(er)? (" + month + r") \d{2,4}", text)
            if match:
                return parse_fr_date(match.group())
        except:
            continue
    return None
