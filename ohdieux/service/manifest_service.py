from ohdieux.model.programme import Programme

class ManifestService(object):

    def generate_podcast_manifest(self, programme_id: str, reverse_segments: bool) -> Programme:
        raise NotImplementedError
