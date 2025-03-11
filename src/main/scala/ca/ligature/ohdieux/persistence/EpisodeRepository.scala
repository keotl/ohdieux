package ca.ligature.ohdieux.persistence

import scala.concurrent.Future

case class EpisodeEntity(
    id: Int,
    title: String,
    description: String,
    programme_id: Int,
    date: String,
    duration: Int,
    is_broadcast_replay: Int
)

trait EpisodeRepository {
  def getById(id: Int): Option[EpisodeEntity]
  def getByProgrammeId(programmeId: Int): Seq[EpisodeEntity]
  def save(entity: EpisodeEntity): Unit
  def countByProgrammeId(programmeId: Int): Int
}
