import unittest
from datetime import datetime

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.transform.reverse_episode_segments import reverse_episode_segments


class ReverseEpisodeSegmentsTests(unittest.TestCase):

    def test_reverse_segments(self):
        with_reversed = reverse_episode_segments(SOME_PROGRAMME)

        self.assertEqual("second", with_reversed.episodes[0].media[0].media_url)
        self.assertEqual("first", with_reversed.episodes[0].media[1].media_url)


SOME_PROGRAMME = Programme(ProgrammeDescriptor("", "", "", "", ""), [
    EpisodeDescriptor(
        "", "", "", datetime.now(), 123,
        [MediaDescriptor("first", "", 1),
         MediaDescriptor("second", "", 2)])
], datetime.now())
