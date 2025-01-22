package ca.ligature.ohdieux.persistence.impl

import ca.ligature.ohdieux.persistence.{
  ProgrammeConfigRepository,
  ProgrammeConfigEntity,
  ProgrammeConfigStatus
}

import play.api.db.Database
import ca.ligature.ohdieux.infrastructure.DatabaseExecutionContext
import javax.inject.Inject
import anorm.*
import scala.util.Try
import java.sql.PreparedStatement

class DatabaseProgrammeConfigRepository @Inject() (
    val db: Database,
    implicit val databaseExecutionContext: DatabaseExecutionContext
) extends ProgrammeConfigRepository {
  db.withConnection(implicit connection => {
    SQL("""CREATE TABLE IF NOT EXISTS programme_config (
programme_id INTEGER UNIQUE,
status TEXT,
message TEXT,
date TEXT,
PRIMARY KEY("programme_id"))""").execute()
  })

  private implicit def programmeStatusParser: Column[ProgrammeConfigStatus] =
    Column.nonNull { (value, meta) =>
      val MetaDataItem(qualified, nullable, clazz) = meta
      val error = TypeDoesNotMatch(
        s"Cannot convert $value: ${value.asInstanceOf[AnyRef].getClass} to ProgrammeConfigStatus for column $qualified"
      )
      value match {
        case text: String =>
          Try(ProgrammeConfigStatus.valueOf(text)).toEither.left.map((v) =>
            error
          )

        case _ => Left(error)
      }
    }

  private val parser: RowParser[ProgrammeConfigEntity] =
    // Known warning false-positive in anorm 2.7.0 when using scala3 enum column
    Macro.namedParser[ProgrammeConfigEntity]

  private implicit val programmeStatusToStatement
      : ToStatement[ProgrammeConfigStatus] =
    new ToStatement[ProgrammeConfigStatus] {
      def set(
          statement: PreparedStatement,
          i: Int,
          value: ProgrammeConfigStatus
      ): Unit =
        statement.setString(i, value.toString())
    }

  private val toParams: ToParameterList[ProgrammeConfigEntity] =
    Macro.toParameters[ProgrammeConfigEntity]

  override def getProgrammeConfig(programmeId: Int): ProgrammeConfigEntity = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM programme_config WHERE programme_id={id}")
          .on("id" -> programmeId)
          .as(parser.singleOpt)(connection)
          .getOrElse(
            ProgrammeConfigEntity(programmeId, ProgrammeConfigStatus.Ok, "", "")
          )
      }
    }
  }

  override def getAllByStatus(
      status: ProgrammeConfigStatus
  ): Seq[ProgrammeConfigEntity] = {
    db.withConnection { connection =>
      {
        SQL("SELECT * FROM programme_config WHERE status={status}")
          .on("status" -> status)
          .as(parser.*)(connection)
      }
    }
  }

  override def saveProgrammeConfig(
      config: ProgrammeConfigEntity
  ): Unit = {
    db.withConnection { connection =>
      {
        val params = toParams(config)
        val names = params.map(_.name)
        val placeholders = names.map { n => s"{$n}" } mkString ", "
        val updatePlaceholders = names.map(p => s"${p}={$p}") mkString ", "
        val generatedStmt =
          s"""INSERT INTO programme_config(${names mkString ", "})
VALUES ($placeholders)
ON CONFLICT DO UPDATE SET ${updatePlaceholders}
"""
        SQL(generatedStmt).on(params*).execute()(connection)
      }
    }
  }

}
