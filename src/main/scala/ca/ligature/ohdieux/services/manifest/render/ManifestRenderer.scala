package ca.ligature.ohdieux.services.manifest.render
import ca.ligature.ohdieux.services.manifest.types.*
import ca.ligature.ohdieux.persistence.ProgrammeManifestView

import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter
import ca.ligature.ohdieux.utils.|>
import ca.ligature.ohdieux.persistence.ProgrammeManifestEpisode
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import CleanTextUtils._

case class ManifestRenderer(
    userOptions: ManifestRenderUserOptions,
    serverOptions: ManifestRenderServerOptions,
    archive: ArchivedFileRepository
) {

  def render(programme: ProgrammeManifestView): RenderedProgrammeManifest = {
    val episodes = (programme.episodes |> applyLimitEpisodesOption)
      .flatMap(e =>
        renderEpisodeSegments(e)
          |> applyReverseOption
      )
      |> applyExcludeReplaysOption

    RenderedProgrammeManifest(
      programmeId = programme.programmeId,
      title = programme.title |> clean,
      description = programme.description |> clean,
      author = programme.author |> clean,
      canonicalUrl = programme.canonicalUrl,
      imageUrl = programme.imageUrl,
      lastChecked = ZonedDateTime
        .parse(programme.lastChecked)
        .format(DateTimeFormatter.RFC_1123_DATE_TIME),
      advertisedEpisodes = programme.advertisedEpisodes,
      episodes = episodes
    ) |> applyServeImagesOption
  }

  private def renderEpisodeSegments(
      e: ProgrammeManifestEpisode
  ): Seq[RenderedManifestEpisode] = {
    e.media.zipWithIndex.map((m, i) =>
      RenderedManifestEpisode(
        uniqueId = s"${e.episodeId}_${i}",
        title = e.title |> clean |> applyTagSegmentsOption(i),
        description = e.description |> clean,
        date = ZonedDateTime
          .parse(e.date)
          .format(DateTimeFormatter.RFC_1123_DATE_TIME),
        duration = e.duration,
        isBroadcastReplay = if (e.isBroadcastReplay > 0) then true else false,
        mediaId = m.mediaId,
        mediaUrl = m.upstreamUrl,
        mediaType = m.mediaType
      )
        |> applyServeMediaOption
        |> applyFavorAacOption
    )
  }

  private def applyTagSegmentsOption(
      mediaIndex: Int
  )(episodeTitle: String): String = {
    if (userOptions.tag_segments) {
      episodeTitle ++ s" (${mediaIndex + 1})"
    } else {
      episodeTitle
    }
  }

  private def applyReverseOption[T](episodes: Seq[T]): Seq[T] = {
    if (userOptions.reverse) {
      episodes.reverse
    } else {
      episodes
    }
  }

  private def applyLimitEpisodesOption[T](episodes: Seq[T]): Seq[T] = {
    if (userOptions.limit_episodes) {
      episodes.take(MAX_EPISODES_LIMIT)
    } else {
      episodes
    }
  }

  private def applyExcludeReplaysOption(
      renderedEpisodes: Seq[RenderedManifestEpisode]
  ): Seq[RenderedManifestEpisode] = {
    if (userOptions.exclude_replays) {
      renderedEpisodes.filter(_.isBroadcastReplay == false)
    } else {
      renderedEpisodes
    }
  }

  private def applyServeImagesOption =
    renderOption(serverOptions.serveArchivedImages)(
      (programme: RenderedProgrammeManifest) =>
        programme.copy(imageUrl =
          s"${serverOptions.imageArchiveBaseUrl}${programme.programmeId}"
        )
    )

  private def applyServeMediaOption =
    renderOption(serverOptions.serveArchivedMedia)(
      (episode: RenderedManifestEpisode) =>
        if (archive.exists(archive.createMediaHandle(episode.mediaId))) {
          episode.copy(
            mediaUrl =
              s"${serverOptions.mediaArchiveBaseUrl}${episode.mediaId}.m4a",
            mediaType = "audio/mpeg"
          )
        } else {
          episode
        }
    )

  private def applyFavorAacOption =
    renderOption(userOptions.favor_aac)((episode: RenderedManifestEpisode) => {
      // blindly replace .mp4 urls with .aac, assuming it exists.
      // This is deprecated, as it does not work reliably for all programmes.
      if (""".*/mp4/.*\.mp4$""".r.matches(episode.mediaUrl)) {
        episode.copy(mediaUrl =
          episode.mediaUrl.replace("/mp4/", "/hls/").replace(".mp4", ".aac")
        )
      } else {
        episode
      }
    })

  private def renderOption[T](
      toggle: Boolean
  )(transform: T => T)(entity: T): T = {
    if (toggle) {
      transform(entity)
    } else {
      entity
    }
  }

}

private val MAX_EPISODES_LIMIT = 50
