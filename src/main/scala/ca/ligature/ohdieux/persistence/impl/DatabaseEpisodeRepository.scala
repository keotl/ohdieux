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
import ca.ligature.ohdieux.persistence.EpisodeRepository
import ca.ligature.ohdieux.persistence.EpisodeEntity

class DatabaseEpisodeRepository @Inject() (
    val db: Database,
    implicit val databaseExecutionContext: DatabaseExecutionContext
) extends EpisodeRepository {

  db.withConnection(implicit connection => {
    SQL("""CREATE TABLE IF NOT EXISTS episodes (
id INTEGER UNIQUE,
programme_id INTEGER,
title TEXT,
description TEXT,
date TEXT,
duration INTEGER,
is_broadcast_replay INTEGER,
PRIMARY KEY("id"))""").execute()
  })

  private val parser: RowParser[EpisodeEntity] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[EpisodeEntity]

  private val toParams: ToParameterList[EpisodeEntity] =
    Macro.toParameters[EpisodeEntity]

  override def getById(id: Int): Option[EpisodeEntity] = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM episodes WHERE id={id}")
          .on("id" -> id)
          .as(parser.singleOpt)(connection)
      }
    }
  }

  override def getByProgrammeId(programmeId: Int): Seq[EpisodeEntity] = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM episodes WHERE programme_id={programme_id}")
          .on("programme_id" -> programmeId)
          .as(parser.*)(connection)
      }
    }
  }

  override def save(entity: EpisodeEntity): Unit = {
    // Future {
    db.withConnection { connection =>
      {
        val params = toParams(entity)
        val names = params.map(_.name)
        val placeholders = names.map { n => s"{$n}" } mkString ", "
        val updatePlaceholders = names.map(p => s"${p}={$p}") mkString ", "
        val generatedStmt =
          s"""INSERT INTO episodes(${names mkString ", "})
VALUES ($placeholders)
ON CONFLICT DO UPDATE SET ${updatePlaceholders}
"""
        SQL(generatedStmt).on(params*).execute()(connection)
      }
    }
    // }
  }

  override def countByProgrammeId(programmeId: Int): Int = {
    db.withConnection { connection =>
      {
        SQL("SELECT COUNT() FROM episodes WHERE programme_id={programme_id}")
          .on("programme_id" -> programmeId)
          .as(SqlParser.scalar[Int].single)(connection)
      }
    }
  }

}
