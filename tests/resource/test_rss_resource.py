import unittest
from datetime import datetime

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.resource.rss_resource import render_episode


class RssResourceTests(unittest.TestCase):

    def test_render_multi_segment_episode(self):
        rendered_episodes = render_episode(MULTI_SEGMENT_EPISODE)

        self.assertEqual(2, len(rendered_episodes))
        self.assertEqual("first", rendered_episodes[0].guid)
        self.assertEqual("first", rendered_episodes[0].media.media_url)
        self.assertEqual("second", rendered_episodes[1].guid)
        self.assertEqual("second", rendered_episodes[1].media.media_url)

    def test_render_multi_segment_tag_episode_title(self):
        rendered_episodes = render_episode(MULTI_SEGMENT_EPISODE, tag_segments=True)

        self.assertEqual(2, len(rendered_episodes))
        self.assertEqual("episode title (1)", rendered_episodes[0].title)
        self.assertEqual("episode title (2)", rendered_episodes[1].title)


MULTI_SEGMENT_EPISODE = EpisodeDescriptor(
    "episode title", "", "", datetime.now(), 123,
    [MediaDescriptor("first", "", 1),
     MediaDescriptor("second", "", 2)])
