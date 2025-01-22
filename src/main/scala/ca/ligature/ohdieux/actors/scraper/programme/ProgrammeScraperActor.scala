package ca.ligature.ohdieux.actors.scraper.programme

import org.apache.pekko.actor.typed.scaladsl.ActorContext
import org.apache.pekko.actor.typed.scaladsl.AbstractBehavior
import org.apache.pekko.actor.typed.Behavior
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import org.apache.pekko.actor.typed.SupervisorStrategy
import ca.ligature.ohdieux.persistence.ProgrammeRepository
import ca.ligature.ohdieux.persistence.EpisodeRepository
import ProgrammeScraperActorImpl._
import ca.ligature.ohdieux.ohdio.ApiClient
import ca.ligature.ohdieux.ohdio.RCModels
import ca.ligature.ohdieux.actors.scraper.media.MediaScraperActor
import org.apache.pekko.actor.typed.ActorRef
import com.google.inject.Provides
import com.google.inject.Inject
import ca.ligature.ohdieux.actors.file.FileArchiveActor
import scala.concurrent.duration.DurationInt
import ca.ligature.ohdieux.persistence.ProgrammeConfigRepository
import ca.ligature.ohdieux.persistence.ProgrammeConfigStatus
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter
import ca.ligature.ohdieux.persistence.ProgrammeConfigEntity

class ProgrammeScraperActor(
    apiClient: ApiClient,
    programmeRepository: ProgrammeRepository,
    episodeRepository: EpisodeRepository,
    programmeConfigRepository: ProgrammeConfigRepository,
    maxDepth: Int,
    context: ActorContext[ProgrammeScraperActor.Message],
    mediaScraper: ActorRef[MediaScraperActor.Message],
    archiveActor: ActorRef[FileArchiveActor.Message]
) extends AbstractBehavior[ProgrammeScraperActor.Message](context) {
  import ProgrammeScraperActor._

  private val impl = ProgrammeScraperActorImpl(
    apiClient,
    programmeRepository,
    episodeRepository,
    maxDepth,
    onNewEpisodeFound,
    onNewProgrammeImage
  )

  override def onMessage(msg: Message): Behavior[Message] = {
    msg match {
      case Message.FetchProgramme(programmeId, incremental) => {
        if (shouldFetchProgramme(programmeId)) {
          try {
            impl.fetchProgramme(programmeId, incremental)
          } catch {
            case e => trackFetchFailure(programmeId, e.getMessage())
          }
        }
      }
      case Message.RefreshAllProgrammesIncrementally() => {
        val programmes = programmeRepository.getAll()
        context.log.info(
          s"Queuing auto-refresh for ${programmes.length} programmes."
        )
        for (programme <- programmes) do {
          context.self ! Message.FetchProgramme(
            programme.id,
            incremental = true
          )
        }

      }
    }

    this
  }

  private def onNewEpisodeFound(
      episode: RCModels.ProgrammeContentDetailItem,
      parentProgrammeId: Int
  ): Unit = {
    mediaScraper ! MediaScraperActor.Message.NewEpisode(
      episode,
      parentProgrammeId
    )
  }
  private def onNewProgrammeImage(programmeId: Int, imageUrl: String): Unit = {
    archiveActor ! FileArchiveActor.Message.SaveImage(programmeId, imageUrl)
  }

  private def shouldFetchProgramme(
      programmeId: Int
  ): Boolean = {
    val config = programmeConfigRepository.getProgrammeConfig(programmeId)
    val notFailed = config.status != ProgrammeConfigStatus.Failed

    notFailed
  }

  private def trackFetchFailure(programmeId: Int, message: String): Unit = {
    programmeConfigRepository.saveProgrammeConfig(
      ProgrammeConfigEntity(
        programmeId,
        ProgrammeConfigStatus.Failed,
        message,
        ZonedDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME)
      )
    )
  }
}

object ProgrammeScraperActor {
  enum Message {
    case FetchProgramme(id: Int, incremental: Boolean = true)
    case RefreshAllProgrammesIncrementally()
  }

  def apply(
      apiClient: ApiClient,
      programmeRepository: ProgrammeRepository,
      episodeRepository: EpisodeRepository,
      programmeConfigRepository: ProgrammeConfigRepository,
      maxDepth: Int,
      mediaScraperRef: ActorRef[MediaScraperActor.Message],
      archiveActorRef: ActorRef[FileArchiveActor.Message],
      refreshInterval: Int
  ): Behavior[Message] =
    Behaviors
      .supervise(Behaviors.setup[Message] { context =>
        Behaviors.withTimers { timers =>
          {
            if (refreshInterval > 0) {
              timers.startTimerAtFixedRate(
                Message.RefreshAllProgrammesIncrementally(),
                refreshInterval.seconds
              )
            }
            new ProgrammeScraperActor(
              apiClient,
              programmeRepository,
              episodeRepository,
              programmeConfigRepository,
              maxDepth,
              context,
              mediaScraperRef,
              archiveActorRef
            )
          }
        }
      })
      .onFailure(SupervisorStrategy.restart)

}
