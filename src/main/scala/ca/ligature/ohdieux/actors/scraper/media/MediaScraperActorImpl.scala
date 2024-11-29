package ca.ligature.ohdieux.actors.scraper.media

import ca.ligature.ohdieux.ohdio.{ApiClient, RCModels}
import ca.ligature.ohdieux.persistence.{
  MediaEntity,
  MediaRepository,
  EpisodeRepository
}
import scala.collection.immutable.HashSet

private case class MediaScraperActorImpl(
    api: ApiClient,
    mediaRepository: MediaRepository,
    episodeRepository: EpisodeRepository,
    archiveBlacklist: HashSet[Int],
    shouldRefreshMediaUrl: (
        mediaId: Int,
        currentUrl: Option[String]
    ) => Boolean,
    onNewMedia: (mediaId: Int, mediaUrl: String, skipDownload: Boolean) => Unit
) {

  def fetchEpisodeMedia(
      episode: RCModels.ProgrammeContentDetailItem,
      parentProgrammeId: Int
  ): Unit = {
    for (mediaId, i) <- fetchMediaIds(episode).zipWithIndex do {
      val alreadySaved = mediaRepository.getById(mediaId.toInt)
      if (
        alreadySaved.isEmpty || shouldRefreshMediaUrl(
          mediaId.toInt,
          alreadySaved.map(_.upstream_url)
        )
      ) {
        val mediaUrl = fetchMediaUrl(mediaId.toInt)
        onNewMedia(
          mediaId.toInt,
          mediaUrl,
          archiveBlacklist.contains(parentProgrammeId)
        )
        mediaRepository.save(
          MediaEntity(
            id = mediaId.toInt,
            episode_id = episode.playlistItemId.globalId2.id.toInt,
            episode_index = i,
            length = episode.duration.durationInSeconds,
            upstream_url = mediaUrl
          )
        )
      }
    }
  }

  def retriggerDownloads(programmeId: Int): Unit = {
    for (episode <- episodeRepository.getByProgrammeId(programmeId)) do {
      val media = mediaRepository.getByEpisodeId(episode.id)
      for (m <- media) do {
        onNewMedia(m.id, m.upstream_url, archiveBlacklist.contains(programmeId))
      }
    }
  }

  private def fetchMediaIds(
      episode: RCModels.ProgrammeContentDetailItem
  ): Seq[String] =
    episode.playlistItemId.mediaId
      .map(Seq(_))
      .getOrElse(
        fetchMediaIdsFromPlaybackList(episode.playlistItemId)
      )

  private def fetchMediaIdsFromPlaybackList(
      playlistItemId: RCModels.PlaylistItemId
  ): Seq[String] = {
    val playbackList = api
      .getPlaybacklistById(
        playlistItemId.globalId2.contentType.id,
        playlistItemId.globalId2.id
      )
      .get

    playbackList.items
      .filter(
        _.mediaPlaybackItem.globalId.id == playlistItemId.globalId2.id
      )
      .map(_.mediaPlaybackItem.mediaId)
      .distinct

  }

  private def fetchMediaUrl(mediaId: Int): String = {
    TECHS
      .flatMap(
        api.getMedia(mediaId, _).opt
      )
      .map(_.url)
      .headOption
      .getOrElse(
        throw new Error(s"Could not fetch stream form media ${mediaId}")
      )
  }

}

private case class MediaUrl(tech: "hls" | "progressive", url: String);

private val TECHS: LazyList["hls" | "progressive"] =
  LazyList("progressive", "hls")
