package ca.ligature.ohdieux.persistence.impl

import javax.inject.Inject
import play.api.db.Database
import ca.ligature.ohdieux.infrastructure.DatabaseExecutionContext

import scala.concurrent.Future
import anorm.*
import scala.util.Try
import scala.util.Failure
import scala.annotation.nowarn
import java.sql.PreparedStatement
import ca.ligature.ohdieux.persistence.MediaRepository
import ca.ligature.ohdieux.persistence.MediaEntity

class DatabaseMediaRepository @Inject() (
    val db: Database,
    implicit val databaseExecutionContext: DatabaseExecutionContext
) extends MediaRepository {

  db.withConnection(implicit connection => {
    SQL("""CREATE TABLE IF NOT EXISTS media (
id INTEGER UNIQUE,
episode_id INTEGER,
episode_index INTEGER,
length INTEGER,
upstream_url TEXT,
PRIMARY KEY("id")
UNIQUE (episode_id,episode_index)
)""").execute()
  })

  private val parser: RowParser[MediaEntity] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[MediaEntity]

  private val toParams: ToParameterList[MediaEntity] =
    Macro.toParameters[MediaEntity]

  override def getById(id: Int): Option[MediaEntity] = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM media WHERE id={id}")
          .on("id" -> id)
          .as(parser.singleOpt)(connection)
      }
    }
  }
  override def getByEpisodeId(episodeId: Int): Seq[MediaEntity] = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM media WHERE episode_id={episode_id}")
          .on("episode_id" -> episodeId)
          .as(parser.*)(connection)
      }
    }
  }

  override def save(entity: MediaEntity): Unit = {
    // Future {
    db.withConnection { connection =>
      {
        val params = toParams(entity)
        val names = params.map(_.name)
        val placeholders = names.map { n => s"{$n}" } mkString ", "
        val updatePlaceholders = names.map(p => s"${p}={$p}") mkString ", "
        val generatedStmt =
          s"""INSERT INTO media(${names mkString ", "})
VALUES ($placeholders)
ON CONFLICT DO UPDATE SET ${updatePlaceholders}
"""
        SQL(generatedStmt).on(params*).execute()(connection)
      }
    }
    // }
  }
}
