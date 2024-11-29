package ca.ligature.ohdieux.persistence.impl

import javax.inject.Inject
import play.api.db.Database
import ca.ligature.ohdieux.infrastructure.DatabaseExecutionContext

import scala.concurrent.Future
import ca.ligature.ohdieux.persistence.{
  ProgrammeEntity,
  ProgrammeRepository,
  ProgrammeType
}
import anorm.*
import scala.util.Try
import scala.util.Failure
import scala.annotation.nowarn
import java.sql.PreparedStatement
import java.sql.Connection

class DatabaseProgrammeRepository @Inject() (
    val db: Database,
    implicit val databaseExecutionContext: DatabaseExecutionContext
) extends ProgrammeRepository {

  db.withConnection(implicit connection => {
    SQL("""CREATE TABLE IF NOT EXISTS programmes (
id INTEGER UNIQUE,
programme_type TEXT,
title TEXT,
description TEXT,
author TEXT,
canonical_url TEXT,
image_url TEXT,
episodes INTEGER,
last_checked TEXT,
PRIMARY KEY("id"))""").execute()
//    connection.commit()
  })

  private implicit def programmeTypeParser: Column[ProgrammeType] =
    Column.nonNull { (value, meta) =>
      val MetaDataItem(qualified, nullable, clazz) = meta
      val error = TypeDoesNotMatch(
        s"Cannot convert $value: ${value.asInstanceOf[AnyRef].getClass} to ProgrammeType for column $qualified"
      )
      value match {
        case text: String =>
          Try(ProgrammeType.valueOf(text)).toEither.left.map((v) => error)

        case _ => Left(error)
      }
    }

  private val parser: RowParser[ProgrammeEntity] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[ProgrammeEntity]

  private implicit val programmeTypeToStatement: ToStatement[ProgrammeType] =
    new ToStatement[ProgrammeType] {
      def set(
          statement: PreparedStatement,
          i: Int,
          value: ProgrammeType
      ): Unit =
        statement.setString(i, value.toString())
    }

  private val toParams: ToParameterList[ProgrammeEntity] =
    Macro.toParameters[ProgrammeEntity]

  override def getById(id: Int): Option[ProgrammeEntity] = {
    db.withConnection { connection =>
      getById(id, connection)
    }
  }

  def getById(id: Int, connection: Connection): Option[ProgrammeEntity] = {
    SQL("SELECT * FROM programmes WHERE id={id}")
      .on("id" -> id)
      .as(parser.singleOpt)(connection)
  }

  override def getAll(): Seq[ProgrammeEntity] = {
    db.withConnection { connection =>
      SQL("SELECT * FROM programmes")
        .as(parser.*)(connection)
    }
  }

  override def save(entity: ProgrammeEntity): Unit = {
    // Future {
    db.withConnection { connection =>
      {
        val params = toParams(entity)
        val names = params.map(_.name)
        val placeholders = names.map { n => s"{$n}" } mkString ", "
        val updatePlaceholders = names.map(p => s"${p}={$p}") mkString ", "
        val generatedStmt =
          s"""INSERT INTO programmes(${names mkString ", "})
VALUES ($placeholders)
ON CONFLICT DO UPDATE SET ${updatePlaceholders}
"""
        SQL(generatedStmt).on(params*).execute()(connection)
      }
    }
    // }
  }
}
