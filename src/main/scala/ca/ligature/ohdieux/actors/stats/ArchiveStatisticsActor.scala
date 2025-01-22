package ca.ligature.ohdieux.actors.stats

import org.apache.pekko.actor.typed.scaladsl.ActorContext
import org.apache.pekko.actor.typed.scaladsl.AbstractBehavior
import org.apache.pekko.actor.typed.Behavior
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import ca.ligature.ohdieux.persistence.StatisticsRepository
import ca.ligature.ohdieux.persistence.ManifestRepository
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import ca.ligature.ohdieux.persistence.ProgrammeArchiveStatistics

class ArchiveStatisticsActor(
    manifestRepository: ManifestRepository,
    statsRepository: StatisticsRepository,
    archive: ArchivedFileRepository,
    context: ActorContext[ArchiveStatisticsActor.Message]
) extends AbstractBehavior[ArchiveStatisticsActor.Message](context) {
  import ArchiveStatisticsActor._

  override def onMessage(msg: Message): Behavior[Message] = {
    msg match {
      case Message.IncrementArchivedCountForProgramme(programmeId) => {
        val stats = statsRepository
          .getProgrammeArchiveStatistics(programmeId)
          .getOrElse(ProgrammeArchiveStatistics(programmeId, 0))

        statsRepository.saveProgrammeArchiveStatistics(
          stats.copy(archived_episodes = stats.archived_episodes + 1)
        )
      }

      case Message.RecomputeArchiveStatistics() => {
        for (programme <- statsRepository.getGlobalStatistics()) {
          val manifest =
            manifestRepository.getProgrammeManifest(programme.programmeId)

          val archivedEpisodes = manifest
            .map(
              _.episodes
                .flatMap(_.media)
                .count(m =>
                  archive.exists(archive.createMediaHandle(m.mediaId))
                )
            )
            .getOrElse(0)

          statsRepository.saveProgrammeArchiveStatistics(
            ProgrammeArchiveStatistics(programme.programmeId, archivedEpisodes)
          )
        }
      }
    }
    this
  }
}

object ArchiveStatisticsActor {
  enum Message {
    case RecomputeArchiveStatistics()
    case IncrementArchivedCountForProgramme(programmeId: Int)
  }

  def apply(
      manifestRepository: ManifestRepository,
      statsRepository: StatisticsRepository,
      archive: ArchivedFileRepository
  ): Behavior[Message] =
    Behaviors.setup(context =>
      new ArchiveStatisticsActor(
        manifestRepository,
        statsRepository,
        archive,
        context
      )
    )

}
