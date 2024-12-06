import argparse
from datetime import timedelta, tzinfo
import itertools
import json
import os.path
import sys
from typing import Iterable, List
import dateutil.parser

def _programme_type(canonical_url: str) -> str:
    if "premiere/emission" in canonical_url:
        return "EmissionPremiere"
    if "balado" in canonical_url:
        return "Balado"
    if "grandes-series" in canonical_url:
        return "GrandeSerie"

    raise Exception("Unsupported programme type")


def _format_str(text: str) -> str:
    return f"""'{text.replace("'", "''")}'"""

def _format_date(text: str) -> str:
    parsed = dateutil.parser.parse(text, ignoretz=True) + timedelta(microseconds=1)
    return f"""'{parsed.isoformat()}Z'"""

def insert_programme_statement(programme_id: int, programme: dict) -> str:
    return f"""INSERT INTO programmes(id, programme_type, title, description, author, canonical_url, image_url, episodes, last_checked)
    VALUES ({programme_id},
    {_format_str(_programme_type(programme["programme"]["link"]))},
    {_format_str(programme["programme"]["title"])},
    {_format_str(programme["programme"]["description"])},
    {_format_str(programme["programme"]["author"])},
    {_format_str(programme["programme"]["link"])},
    {_format_str(programme["programme"]["image_url"])},
    {len(programme["episodes"])},
    {_format_date(programme["build_date"])});
    """


def insert_episode_statement(programme_id: int, episode: dict) -> str:
    return f"""INSERT INTO episodes(id, title, description, programme_id, date, duration, is_broadcast_replay)
    VALUES ({episode["guid"]},
    {_format_str(episode["title"])},
    {_format_str(episode["description"])},
    {programme_id},
    {_format_date(episode["date"])},
    {episode["duration"]},
    {int(episode.get("is_broadcast_replay", False) or False)});
    """


def insert_media_statements(episode: dict) -> Iterable[str]:
    for i, media in enumerate(episode["media"]):
        yield f"""INSERT INTO media(id, episode_id, episode_index, length, upstream_url)
        VALUES({-int(episode["guid"]) * 1000 - i},
        {episode["guid"]},
        {i},
        {media["length"]},
        {_format_str(media["media_url"])});
        """


def main(output_file: str, filenames: List[str], programme_id_arg: str,
         force_preserve_media: bool):
    output_statements = []
    for file in filenames:
        with open(file, "r") as f:
            programme = json.load(f)
        programme_id = int((os.path.basename(file)).replace(
            ".json",
            "")) if programme_id_arg == "INFER" else int(programme_id_arg)
        try:
            output_statements.append(
                insert_programme_statement(programme_id, programme))
            output_statements.extend(
                map(lambda e: insert_episode_statement(programme_id, e),
                    programme["episodes"]))
            if force_preserve_media:
                output_statements.extend(
                    itertools.chain(
                        *map(insert_media_statements, programme["episodes"])))
        except:
            continue

    with open(output_file, "w") as f:
        f.write("\n".join(output_statements))


parser = argparse.ArgumentParser(
    prog='import_v1_data',
    description='Generate SQL statements to import json-exported v1 programmes.'
)

parser.add_argument("filename", nargs="+", help=".json file(s) to import")
parser.add_argument("-o",
                    "--output",
                    dest="output",
                    help="output .sql file.",
                    default="output.sql")
parser.add_argument(
    "--programme-id",
    dest="programme_id",
    help="Programme ID to import. Defaults to infer from filename.",
    default="INFER")
parser.add_argument(
    "--force-preserve-media",
    action="store_true",
    dest="force_preserve_media",
    help="""Create fake media entries to retain saved media_urls.
    V1 did not store media IDs, so we have to invent a media ID based on the episode ID.
    Invented media IDs will be *negative*, so removing them can be done afterwards by filtering on the media table where id < 0."""
)

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1::])
    main(args.output, args.filename, args.programme_id,
         args.force_preserve_media)
