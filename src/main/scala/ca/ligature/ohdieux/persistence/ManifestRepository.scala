package ca.ligature.ohdieux.persistence

trait ManifestRepository {
  def getProgrammeManifest(programmeId: Int): Option[ProgrammeManifestView]
}

case class ProgrammeManifestView(
    programmeId: Int,
    title: String,
    description: String,
    author: String,
    canonicalUrl: String,
    imageUrl: String,
    lastChecked: String,
    advertisedEpisodes: Int,
    episodes: Seq[ProgrammeManifestEpisode]
)

case class ProgrammeManifestEpisode(
    episodeId: Int,
    title: String,
    description: String,
    date: String,
    duration: Int,
    isBroadcastReplay: Int,
    media: Seq[EpisodeMediaStream]
)

case class EpisodeMediaStream(
    mediaId: Int,
    upstreamUrl: String,
    mediaType: String
)
