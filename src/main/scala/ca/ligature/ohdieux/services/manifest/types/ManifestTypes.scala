package ca.ligature.ohdieux.services.manifest.types

case class ManifestRenderUserOptions(
    reverse: Boolean,
    tag_segments: Boolean,
    limit_episodes: Boolean,
    exclude_replays: Boolean
)

case class ManifestRenderServerOptions(
    serveArchivedImages: Boolean,
    imageArchiveBaseUrl: String = "/media/images/",
    serveArchivedMedia: Boolean,
    mediaArchiveBaseUrl: String = "/media/audio/",
    autoAddProgrammes: Boolean
)

case class RenderedProgrammeManifest(
    programmeId: Int,
    title: String,
    description: String,
    author: String,
    canonicalUrl: String,
    imageUrl: String,
    lastChecked: String,
    advertisedEpisodes: Int,
    episodes: Seq[RenderedManifestEpisode]
)

case class RenderedManifestEpisode(
    uniqueId: String,
    title: String,
    description: String,
    date: String,
    duration: Int,
    isBroadcastReplay: Boolean,
    mediaId: Int,
    mediaUrl: String,
    mediaType: String
)
