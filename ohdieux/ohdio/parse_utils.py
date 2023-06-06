from ohdieux.util.xml import unsafe_strip_tags


def clean(human_readable_text: str) -> str:
    return unsafe_strip_tags(human_readable_text or "") \
        .replace("&nbsp;", " ") \
        .replace("&", "&amp; ")
