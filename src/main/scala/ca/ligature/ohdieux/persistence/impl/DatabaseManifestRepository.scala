package ca.ligature.ohdieux.persistence.impl
import play.api.db.Database

import ca.ligature.ohdieux.infrastructure.DatabaseExecutionContext
import javax.inject.Inject
import ca.ligature.ohdieux.persistence._
import anorm.*

class DatabaseProgrammeManifestRepository @Inject() (
    val db: Database,
    val programmeRepository: DatabaseProgrammeRepository,
    implicit val databaseExecutionContext: DatabaseExecutionContext
) extends ManifestRepository {

  val episodesByProgrammeIdQuery = SQL("""SELECT
episodes.id as episode_id,
episodes.title as episode_title,
episodes.description as episode_description,
episodes.date as episode_date,
episodes.is_broadcast_replay as is_broadcast_replay,
episodes.duration as episode_duration,
media.id as media_id,
media.upstream_url as media_upstream_url,
media.episode_index as media_episode_index,
programmes.image_url as image_url
 FROM episodes
  INNER JOIN media ON episodes.id = media.episode_id
  INNER JOIN programmes ON episodes.programme_id = programmes.id
  WHERE episodes.programme_id = {programme_id}
  ORDER BY episode_id DESC;
""")

  case class EpisodeQueryResult(
      episode_id: Int,
      episode_title: String,
      episode_description: String,
      episode_date: String,
      is_broadcast_replay: Int,
      episode_duration: Int,
      media_id: Int,
      media_upstream_url: String,
      media_episode_index: Int,
      image_url: String
  )

  private val parser: RowParser[EpisodeQueryResult] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[EpisodeQueryResult]

  def getProgrammeManifest(programmeId: Int): Option[ProgrammeManifestView] = {
    db.withConnection { connection =>
      {
        val programme = programmeRepository.getById(programmeId, connection)
        val episodes =
          episodesByProgrammeIdQuery
            .on("programme_id" -> programmeId)
            .as(parser.*)(connection)

        programme.map((p) =>
          ProgrammeManifestView(
            programmeId = p.id,
            title = p.title,
            description = p.description,
            author = p.author,
            canonicalUrl = p.canonical_url,
            imageUrl = p.image_url,
            lastChecked = p.last_checked,
            advertisedEpisodes = p.episodes,
            episodes = assembleEpisodes(episodes)
          )
        )
      }
    }
  }

  private def assembleEpisodes(
      episodeResults: Seq[EpisodeQueryResult]
  ): Seq[ProgrammeManifestEpisode] = {
    val grouped = episodeResults.groupBy(_.episode_id)

    def assembleEpisode(episodeId: Int): ProgrammeManifestEpisode = {
      val segments = grouped(episodeId).sortBy(_.media_episode_index)
      ProgrammeManifestEpisode(
        episodeId = episodeId,
        title = segments.head.episode_title,
        description = segments.head.episode_description,
        date = segments.head.episode_date,
        duration = segments.head.episode_duration,
        isBroadcastReplay = segments.head.is_broadcast_replay,
        media = segments.map(m =>
          EpisodeMediaStream(m.media_id, m.media_upstream_url, "audio/mpeg")
        )
      )

    }

    episodeResults
      .map(_.episode_id)
      .distinct
      .map(assembleEpisode)
  }

}
