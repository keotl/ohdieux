import logging
import os

import requests
from jivago.inject.annotation import Component, Provider

if os.environ.get("USER_AGENT"):
    USER_AGENT = {"User-Agent": os.environ.get("USER_AGENT") or ""}
else:
    USER_AGENT = None


class ApiException(Exception):
    pass


@Component
class OhdioApi(object):

    def __init__(
        self,
        base_url:
        str = "https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes-v2/"
    ) -> None:
        self.base_url = base_url
        self._logger = logging.getLogger(self.__class__.__name__)

    def query_episodes(self, programme_id: str, page_number) -> dict:
        self._logger.debug(
            f"Querying episodes for programme: {programme_id}/{page_number}.")
        response = requests.get(self.base_url + programme_id + "/" +
                                str(page_number),
                                headers=USER_AGENT)
        if response.ok:
            return response.json()
        else:
            self._logger.debug(
                f"Failed to retrieve page number {page_number}.")
            raise ApiException(response.text)

    # def query_episode_segments(self, programme_id: str,
    #                            episode_id: str,
    #                            playlist_item_id: str) -> dict:
    #     self._logger.debug(
    #         f"Querying episode segments for programme: {programme_id}/{episode_id}."
    #     )

    #     if episode_id is not None:
    #         response = requests.get(
    #         f"https://services.radio-canada.ca/neuro/sphere/v1/medias/apps/playback-lists/{playlist_item_id}?context=web&globalId={playlist_item_id}",
    #         # f"https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes/{programme_id}/episodes/{episode_id}",
    #         timeout=10,
    #         headers=USER_AGENT)
    #     else:
    #         response = requests.get(
    #         f"https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes/{programme_id}/episodes/{playlist_item_id.split('-')[-1]}",
    #         timeout=10,
    #         headers=USER_AGENT)
    #     if response.ok:
    #         return response.json()["items"]
    #     else:
    #         self._logger.debug(
    #             f"Failed to retrieve segments for episode {episode_id}.",
    #             response.text)
    #         raise ApiException(response.text)

    def query_programme(self, programme_id: str) -> dict:
        response = requests.get(self.base_url + programme_id,
                                headers=USER_AGENT)
        if response.ok:
            return response.json()
        else:
            self._logger.debug(f"Failed to retrieve programme {programme_id}.")
            raise ApiException(response.text)

    def query_media(self, media_id: str) -> dict:
        response = requests.get(
            f"https://services.radio-canada.ca/media/validation/v2/?appCode=medianet&connectionType=hd&deviceType=ipad&idMedia={media_id}&multibitrate=true&output=json&tech=progressive",
            headers=USER_AGENT)
        if response.ok:
            return response.json()
        else:
            self._logger.debug(f"Failed to retrieve media for {media_id}.")
            raise ApiException(response.text)


@Provider
def ohdio_api_provider() -> OhdioApi:
    return OhdioApi()
