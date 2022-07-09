from datetime import datetime

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

def parse_fr_date(formatted: str) -> datetime:
    day, month, year = formatted.lower().split(" ")
    return datetime(int(year), MONTHS[month], int(day))
