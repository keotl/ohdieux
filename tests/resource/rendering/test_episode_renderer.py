import unittest
from datetime import datetime

from jivago.lang.stream import Stream
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.resource.rendering.episode_renderer import renderer


class EpisodeRendererTests(unittest.TestCase):

    def test_reverse_episode_segments(self):
        render = renderer(reverse_segments=True)

        res = render(PROGRAMME)

        episodes = Stream(res.episodes).toList()
        self.assertEqual("second", episodes[0].media.media_url)
        self.assertEqual("first", episodes[1].media.media_url)

    def test_render_multi_segment_episode(self):
        render = renderer()

        rendered_programme = render(PROGRAMME)

        rendered_episodes = Stream(rendered_programme.episodes).toList()
        self.assertEqual(2, len(rendered_episodes))
        self.assertEqual("episodeid_0", rendered_episodes[0].guid)
        self.assertEqual("first", rendered_episodes[0].media.media_url)
        self.assertEqual("episodeid_1", rendered_episodes[1].guid)
        self.assertEqual("second", rendered_episodes[1].media.media_url)

    def test_render_multi_segment_tag_episode_title(self):
        render = renderer(tag_segments=True)

        rendered_programme = render(PROGRAMME)

        rendered_episodes = Stream(rendered_programme.episodes).toList()
        self.assertEqual("episode title (1)", rendered_episodes[0].title)
        self.assertEqual("episode title (2)", rendered_episodes[1].title)

    def test_render_replacing_mp4_urls_with_aac(self):
        # Given
        episode = EpisodeDescriptor("", "", "", datetime.now(), 123, [
            MediaDescriptor("example.com/mp4/file.mp4", "", 1),
            MediaDescriptor("untouched", "", 2)
        ])
        programme = Programme(PROGRAMME.programme, [episode], datetime.now())
        render = renderer(favor_aac=True)

        # When
        rendered_programme = render(programme)

        # Then
        rendered_episodes = Stream(rendered_programme.episodes).toList()
        self.assertEqual("example.com/hls/file.aac",
                         rendered_episodes[0].media.media_url)
        self.assertEqual("untouched", rendered_episodes[1].media.media_url)

    def test_render_limit_number_of_episodes(self):
        # Given
        programme = Programme(PROGRAMME.programme, [EPISODE for _ in range(100)],
                              datetime.now())
        render = renderer(limit_episodes=True)

        # When
        rendered_programme = render(programme)

        # Then
        rendered_episodes = Stream(rendered_programme.episodes).toList()
        self.assertEqual(50, len(rendered_episodes))


EPISODE = EpisodeDescriptor(
    "episode title", "description", "episodeid", datetime.now(), 123,
    [MediaDescriptor("first", "", 1),
     MediaDescriptor("second", "", 2)])

PROGRAMME = Programme(programme=ProgrammeDescriptor("title", "description", "author",
                                                    "link", "image_url"),
                      episodes=[EPISODE],
                      build_date=datetime.now())
