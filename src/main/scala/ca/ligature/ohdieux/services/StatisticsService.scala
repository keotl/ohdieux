package ca.ligature.ohdieux.services

import ca.ligature.ohdieux.persistence.ProgrammeRepository
import javax.inject.Inject
import ca.ligature.ohdieux.persistence.EpisodeRepository
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import ca.ligature.ohdieux.persistence.ManifestRepository
import ca.ligature.ohdieux.persistence.ProgrammeManifestEpisode
import ca.ligature.ohdieux.persistence.ProgrammeStatistics
import ca.ligature.ohdieux.persistence.StatisticsRepository

case class GlobalStatistics(programmes: Seq[ProgrammeStatistics])

case class StatisticsService @Inject() (
    val programmeRepository: ProgrammeRepository,
    val episodeRepository: EpisodeRepository,
    val statisticsRepository: StatisticsRepository,
    val archive: ArchivedFileRepository
) {
  def getGlobalStatistics(): GlobalStatistics = {
    GlobalStatistics(statisticsRepository.getGlobalStatistics())
  }
}
