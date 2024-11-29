package ca.ligature.ohdieux.services

import ca.ligature.ohdieux.persistence.ProgrammeRepository
import javax.inject.Inject
import ca.ligature.ohdieux.persistence.EpisodeRepository
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import ca.ligature.ohdieux.persistence.ManifestRepository
import ca.ligature.ohdieux.persistence.ProgrammeManifestEpisode

case class GlobalStatistics(programmes: Seq[ProgrammeStatistics])
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

case class StatisticsService @Inject() (
    val programmeRepository: ProgrammeRepository,
    val episodeRepository: EpisodeRepository,
    val manifestRepository: ManifestRepository,
    val archive: ArchivedFileRepository
) {
  def getGlobalStatistics(): GlobalStatistics = {
    val allProgrammes = programmeRepository.getAll()

    val programmeStats =
      allProgrammes
        .map(p => manifestRepository.getProgrammeManifest(p.id))
        .flatten
        .map(p => {
          ProgrammeStatistics(
            p.programmeId,
            p.title,
            p.advertisedEpisodes,
            p.episodes.length,
            countArchivedEpisodes(p.episodes)
          )
        })

    GlobalStatistics(programmeStats)
  }

  private def countArchivedEpisodes(
      episodes: Seq[ProgrammeManifestEpisode]
  ): Int = {
    episodes
      .map(e => {
        e.media
          .map(m => archive.createMediaHandle(m.mediaId))
          .count(archive.exists)
      })
      .sum
  }
}
