package ca.ligature.ohdieux.actors.scraper.media

import org.apache.pekko.actor.typed.scaladsl.ActorContext
import org.apache.pekko.actor.typed.scaladsl.AbstractBehavior
import org.apache.pekko.actor.typed.scaladsl.AskPattern.*
import org.apache.pekko.actor.typed.{
  ActorRef,
  ActorSystem,
  Behavior,
  SupervisorStrategy
}
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import ca.ligature.ohdieux.persistence.EpisodeEntity
import ca.ligature.ohdieux.ohdio.ApiClient
import ca.ligature.ohdieux.persistence.{MediaRepository, EpisodeRepository}

import ca.ligature.ohdieux.ohdio.RCModels
import ca.ligature.ohdieux.actors.file.FileArchiveActor
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository

import scala.util.Try
import scala.concurrent.duration.*
import org.apache.pekko.util.Timeout

import java.util.concurrent.TimeoutException
import scala.concurrent.Await
import scala.collection.immutable.HashSet

class MediaScraperActor(
    apiClient: ApiClient,
    mediaRepository: MediaRepository,
    episodeRepository: EpisodeRepository,
    fileArchiver: ActorRef[FileArchiveActor.Message],
    archive: ArchivedFileRepository,
    shouldArchiveMedia: Boolean,
    archiveBlacklist: HashSet[Int],
    context: ActorContext[MediaScraperActor.Message]
) extends AbstractBehavior[MediaScraperActor.Message](context) {
  import MediaScraperActor._
  val impl = new MediaScraperActorImpl(
    apiClient,
    mediaRepository,
    episodeRepository,
    archiveBlacklist,
    shouldRefreshMediaUrl,
    onNewMedia
  )
  if (archiveBlacklist.nonEmpty) {
    context.log.info(s"Using programme archive blacklist ${archiveBlacklist}")
  }
  override def onMessage(msg: Message): Behavior[Message] = {
    msg match {
      case Message.NewEpisode(episode, parentProgrammeId) => {
        impl.fetchEpisodeMedia(episode, parentProgrammeId)
      }
      case Message.RetriggerDownloads(programmeId) => {
        impl.retriggerDownloads(programmeId)
      }
    }
    this
  }

  private def onNewMedia(
      mediaId: Int,
      mediaUrl: String,
      skipDownload: Boolean
  ): Unit = {
    fileArchiver ! FileArchiveActor.Message.SaveMedia(
      mediaId,
      mediaUrl,
      skipDownload
    )
  }

  private def shouldRefreshMediaUrl(
      mediaId: Int,
      currentUrl: Option[String]
  ): Boolean = {
    currentUrl match {
      case None => true
      case Some(url) => {
        // TODO - Check if url is ephemeral and has expired  - keotl 2024-11-28
        shouldArchiveMedia && !archive.exists(
          archive.createMediaHandle(mediaId)
        )
      }
    }

  }
}

object MediaScraperActor {
  enum Message {
    case NewEpisode(
        episode: RCModels.ProgrammeContentDetailItem,
        parentProgrammeId: Int
    )
    case RetriggerDownloads(programmeId: Int)
  }

  def apply(
      apiClient: ApiClient,
      mediaRepository: MediaRepository,
      episodeRepository: EpisodeRepository,
      fileArchiver: ActorRef[FileArchiveActor.Message],
      archive: ArchivedFileRepository,
      shouldArchiveMedia: Boolean,
      archiveBlacklist: HashSet[Int]
  ): Behavior[Message] =
    Behaviors
      .supervise(Behaviors.setup[Message] { context =>
        new MediaScraperActor(
          apiClient,
          mediaRepository,
          episodeRepository,
          fileArchiver,
          archive,
          shouldArchiveMedia,
          archiveBlacklist,
          context
        )
      })
      .onFailure(SupervisorStrategy.restart)

}
