package ca.ligature.ohdieux.persistence

trait ProgrammeConfigRepository {
  def getProgrammeConfig(programmeId: Int): ProgrammeConfigEntity
  def saveProgrammeConfig(config: ProgrammeConfigEntity): Unit
  def getAllByStatus(status: ProgrammeConfigStatus): Seq[ProgrammeConfigEntity]
}

enum ProgrammeConfigStatus {
  case Ok, Failed;
}

case class ProgrammeConfigEntity(
    programme_id: Int,
    status: ProgrammeConfigStatus,
    message: String,
    date: String
)
