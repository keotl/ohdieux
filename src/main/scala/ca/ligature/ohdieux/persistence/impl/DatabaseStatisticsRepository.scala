package ca.ligature.ohdieux.persistence.impl

import ca.ligature.ohdieux.infrastructure.DatabaseExecutionContext
import play.api.db.Database
import javax.inject.Inject
import ca.ligature.ohdieux.persistence.StatisticsRepository
import ca.ligature.ohdieux.persistence.ProgrammeStatistics
import anorm.*
import ca.ligature.ohdieux.persistence.ProgrammeArchiveStatistics

class DatabaseStatisticsRepository @Inject() (
    val db: Database,
    val programmeRepository: DatabaseProgrammeRepository,
    implicit val databaseExecutionContext: DatabaseExecutionContext
) extends StatisticsRepository {

  val query = SQL("""SELECT
programmes.id as programme_id,
programmes.title as title,
programmes.episodes as advertised_episodes,
archive_stats.archived_episodes as archived_episodes,
COUNT() as known_episodes
FROM programmes
  INNER JOIN episodes ON programmes.id = episodes.programme_id
  INNER JOIN archive_stats ON programmes.id = archive_stats.programme_id
  GROUP BY programmes.id
  ORDER BY programmes.id ASC;""")

  case class QueryResult(
      programme_id: Int,
      title: String,
      advertised_episodes: Int,
      archived_episodes: Int,
      known_episodes: Int
  )
  private val queryResultParser: RowParser[QueryResult] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[QueryResult]

  override def getGlobalStatistics(): Seq[ProgrammeStatistics] = {
    db.withConnection { implicit connection =>
      {
        val results = query.as(queryResultParser.*)
        results.map(r =>
          ProgrammeStatistics(
            programmeId = r.programme_id,
            title = r.title,
            advertisedEpisodes = r.advertised_episodes,
            knownEpisodes = r.known_episodes,
            archivedEpisodes = r.archived_episodes
          )
        )
      }
    }
  }

  db.withConnection(implicit connection => {
    SQL("""CREATE TABLE IF NOT EXISTS archive_stats (
programme_id INTEGER UNIQUE,
archived_episodes INTEGER,
PRIMARY KEY("programme_id"))""").execute()
  })

  private val toParams: ToParameterList[ProgrammeArchiveStatistics] =
    Macro.toParameters[ProgrammeArchiveStatistics]

  override def saveProgrammeArchiveStatistics(
      entity: ProgrammeArchiveStatistics
  ): Unit = {
    db.withConnection { connection =>
      {
        val params = toParams(entity)
        val names = params.map(_.name)
        val placeholders = names.map { n => s"{$n}" } mkString ", "
        val updatePlaceholders = names.map(p => s"${p}={$p}") mkString ", "
        val generatedStmt =
          s"""INSERT INTO archive_stats(${names mkString ", "})
VALUES ($placeholders)
ON CONFLICT DO UPDATE SET ${updatePlaceholders}
"""
        SQL(generatedStmt).on(params*).execute()(connection)
      }
    }
  }
  private val archiveStatsParser: RowParser[ProgrammeArchiveStatistics] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[ProgrammeArchiveStatistics]
  override def getProgrammeArchiveStatistics(
      programmeId: Int
  ): Option[ProgrammeArchiveStatistics] = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM archive_stats WHERE programme_id={programme_id}")
          .on("programme_id" -> programmeId)
          .as(archiveStatsParser.singleOpt)(connection)
      }
    }
  }
}
