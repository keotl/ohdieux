package ca.ligature.ohdieux.persistence

import javax.inject.Inject
import play.api.db.Database
import ca.ligature.ohdieux.infrastructure.DatabaseExecutionContext
import scala.concurrent.Future

enum ProgrammeType {
  case Balado, EmissionPremiere, GrandeSerie, Audiobook;
}
case class ProgrammeEntity(
    id: Int,
    programme_type: ProgrammeType,
    title: String,
    description: String,
    author: String,
    canonical_url: String,
    image_url: String,
    episodes: Int,
    last_checked: String
)

trait ProgrammeRepository {
  def getById(id: Int): Option[ProgrammeEntity]
  def save(entity: ProgrammeEntity): Unit
  def getAll(): Seq[ProgrammeEntity]
}
