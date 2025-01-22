package ca.ligature.ohdieux.persistence

trait StatisticsRepository {
  def getGlobalStatistics(): Seq[ProgrammeStatistics]
  def saveProgrammeArchiveStatistics(entity: ProgrammeArchiveStatistics): Unit
  def getProgrammeArchiveStatistics(
      programmeId: Int
  ): Option[ProgrammeArchiveStatistics]
}

case class ProgrammeStatistics(
    programmeId: Int,
    title: String,

    // From RC paged configuration
    advertisedEpisodes: Int,

    // Episodes with saved metadata ('episodes' table)
    knownEpisodes: Int,

    // Episodes with saved audio files (if enabled)
    archivedEpisodes: Int
)

case class ProgrammeArchiveStatistics(programme_id: Int, archived_episodes: Int)
