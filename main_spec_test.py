import asyncio
import os
from datetime import datetime
from typing import cast

from pydantic import TypeAdapter

from ohdieux.ohdio.api_client import ApiClient
from ohdieux.ohdio.programme_type import ProgrammeType
from ohdieux.ohdio.types import (MediaStreamDescriptor, PlaybackList,
                                 ProgrammeWithoutCuesheet)


async def main(programme_id: int, programme_type: ProgrammeType):
    programme_validator = TypeAdapter(ProgrammeWithoutCuesheet)
    playback_list_validator = TypeAdapter(PlaybackList)
    media_validator = TypeAdapter(MediaStreamDescriptor)

    client = ApiClient(os.getenv("API_BASE_URL") or "", os.getenv("USER_AGENT") or "")
    programme = await client.get_programme_by_id(programme_id, 1, programme_type)
    import json
    print(json.dumps(programme))

    programme_validator.validate_python(programme, strict=True)

    for item in programme["content"]["contentDetail"]["items"]:
        playlist_item_id = item['playlistItemId']['globalId2']['id']
        content_type_id = item['playlistItemId']['globalId2']['contentType']['id']
        playback_list = await client.get_playback_list_by_id(content_type_id,
                                                             str(playlist_item_id))

        playback_list_validator.validate_python(playback_list)

        for playback_list_item in playback_list['items']:
            broadcast_date = datetime.strptime(
                playback_list_item['broadcastedFirstTimeAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
            assert broadcast_date
            media_stream = await client.get_media_stream(
                int(playback_list_item['mediaPlaybackItem']['mediaId']), "progressive")

            media_validator.validate_python(media_stream)
            break
        break


if __name__ == '__main__':
    for programme_id, programme_type in [(9887, "balado"), (4586, "emissionpremiere"),
                                         (3858, "emissionpremiere"),
                                         (672, "emissionpremiere"), (7135, "balado")]:
        asyncio.run(main(programme_id, cast(ProgrammeType, programme_type)))
