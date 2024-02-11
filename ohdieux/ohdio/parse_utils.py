import html
from xml.sax import saxutils as xml

from ohdieux.util.xml import unsafe_strip_tags


def clean(human_readable_text: str) -> str:
    return xml.escape(html.unescape(unsafe_strip_tags(human_readable_text or "")))
