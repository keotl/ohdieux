import re

PATTERN = re.compile(r"<[^<]+?>")

def unsafe_strip_tags(text: str) -> str:
    return PATTERN.sub("", text)
