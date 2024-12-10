package ca.ligature.ohdieux.services

import ca.ligature.ohdieux.persistence.ProgrammeRepository
import javax.inject.Inject
import ca.ligature.ohdieux.persistence.EpisodeRepository
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import ca.ligature.ohdieux.persistence.ManifestRepository
import ca.ligature.ohdieux.persistence.ProgrammeManifestEpisode
import ca.ligature.ohdieux.persistence.ProgrammeStatistics
import ca.ligature.ohdieux.persistence.StatisticsRepository
import ca.ligature.ohdieux.persistence.ProgrammeConfigRepository
import ca.ligature.ohdieux.persistence.ProgrammeConfigStatus
import ca.ligature.ohdieux.persistence.ProgrammeConfigEntity

case class GlobalStatistics(
    programmes: Seq[ProgrammeStatistics],
    failures: Seq[ProgrammeConfigEntity]
)

case class StatisticsService @Inject() (
    val programmeRepository: ProgrammeRepository,
    val episodeRepository: EpisodeRepository,
    val statisticsRepository: StatisticsRepository,
    val programmeConfigRepository: ProgrammeConfigRepository,
    val archive: ArchivedFileRepository
) {
  def getGlobalStatistics(): GlobalStatistics = {
    GlobalStatistics(
      statisticsRepository.getGlobalStatistics(),
      programmeConfigRepository
        .getAllByStatus(ProgrammeConfigStatus.Failed)
    )
  }
}
