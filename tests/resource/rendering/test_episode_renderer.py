import unittest
from datetime import datetime

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.resource.rendering.episode_renderer import renderer


class EpisodeRendererTests(unittest.TestCase):

    def test_reverse_episode_segments(self):
        render = renderer(reverse_segments=True)

        res = render(SOME_EPISODE)

        self.assertEqual("second", res[0].media.media_url)
        self.assertEqual("first", res[1].media.media_url)

    def test_render_multi_segment_episode(self):
        render = renderer()

        rendered_episodes = render(SOME_EPISODE)

        self.assertEqual(2, len(rendered_episodes))
        self.assertEqual("episodeid_0", rendered_episodes[0].guid)
        self.assertEqual("first", rendered_episodes[0].media.media_url)
        self.assertEqual("episodeid_1", rendered_episodes[1].guid)
        self.assertEqual("second", rendered_episodes[1].media.media_url)

    def test_render_multi_segment_tag_episode_title(self):
        render = renderer(tag_segments=True)

        rendered_episodes = render(SOME_EPISODE)

        self.assertEqual("episode title (1)", rendered_episodes[0].title)
        self.assertEqual("episode title (2)", rendered_episodes[1].title)

    def test_render_replacing_mp4_urls_with_aac(self):
        # Given
        episode = EpisodeDescriptor("", "", "", datetime.now(), 123, [
            MediaDescriptor("example.com/mp4/file.mp4", "", 1),
            MediaDescriptor("untouched", "", 2)
        ])
        render = renderer(favor_aac=True)

        # When
        rendered_episodes = render(episode)

        # Then
        self.assertEqual("example.com/hls/file.aac",
                         rendered_episodes[0].media.media_url)
        self.assertEqual("untouched", rendered_episodes[1].media.media_url)


SOME_EPISODE = EpisodeDescriptor(
    "episode title", "description", "episodeid", datetime.now(), 123,
    [MediaDescriptor("first", "", 1),
     MediaDescriptor("second", "", 2)])
