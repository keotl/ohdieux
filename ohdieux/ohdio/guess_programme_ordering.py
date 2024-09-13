from datetime import timezone
from typing import List, Literal

from ohdieux.model.episode_descriptor import EpisodeDescriptor


def guess_programme_ordering(
    episodes: List[EpisodeDescriptor]
) -> Literal["oldest_to_newest", "newest_to_oldest", "unknown"]:
    previous_timestamp = None
    ordering_guess = 0

    for episode in episodes:
        if abs(ordering_guess) > 5:
            break

        if episode.is_broadcast_replay:
            continue

        if previous_timestamp is None:
            previous_timestamp = episode.date

        else:

            if previous_timestamp.astimezone(  # type: ignore[unreachable]
                    timezone.utc) < episode.date.astimezone(timezone.utc):
                ordering_guess += 1
            elif previous_timestamp.astimezone(timezone.utc) > episode.date.astimezone(
                    timezone.utc):
                ordering_guess -= 1

            previous_timestamp = episode.date

    if ordering_guess > 0:
        return "oldest_to_newest"
    if ordering_guess < 0:
        return "newest_to_oldest"

    return "unknown"
