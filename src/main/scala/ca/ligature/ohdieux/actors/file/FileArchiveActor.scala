package ca.ligature.ohdieux.actors.file

import org.apache.pekko.actor.typed.scaladsl.ActorContext
import org.apache.pekko.actor.typed.scaladsl.AbstractBehavior
import org.apache.pekko.actor.typed.Behavior
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import ca.ligature.ohdieux.actors.file.impl.FileArchiveActorImpl
import org.apache.pekko.actor.typed.SupervisorStrategy
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import org.apache.pekko.actor.typed.ActorRef
import ca.ligature.ohdieux.actors.stats.ArchiveStatisticsActor

class FileArchiveActor(
    impl: FileArchiveActorImpl,
    statsActor: ActorRef[ArchiveStatisticsActor.Message],
    context: ActorContext[FileArchiveActor.Message]
) extends AbstractBehavior[FileArchiveActor.Message](context) {
  import FileArchiveActor._

  override def onMessage(msg: Message): Behavior[Message] = {
    msg match {
      case Message.SaveImage(programmeId, imageUrl) =>
        impl.saveImage(programmeId, imageUrl)
      case Message.SaveMedia(
            mediaId,
            upstreamUrl,
            skipDownload,
            parentProgrammeId
          ) =>
        impl.saveMedia(
          mediaId,
          upstreamUrl,
          skipDownload,
          parentProgrammeId,
          onNewFileSaved
        )
    }
    this
  }

  private def onNewFileSaved(programmeId: Int): Unit = {
    statsActor.tell(
      ArchiveStatisticsActor.Message.IncrementArchivedCountForProgramme(
        programmeId
      )
    )
  }
}

object FileArchiveActor {
  enum Message {
    case SaveImage(programmeId: Int, imageUrl: String)
    case SaveMedia(
        mediaId: Int,
        upstreamUrl: String,
        skipDownload: Boolean,
        parentProgrammeId: Int
    )
  }

  def apply(
      statsActor: ActorRef[ArchiveStatisticsActor.Message],
      archive: ArchivedFileRepository,
      userAgent: String,
      archiveMedia: Boolean
  ): Behavior[Message] =
    Behaviors
      .supervise(
        Behaviors.setup(context =>
          new FileArchiveActor(
            new FileArchiveActorImpl(archive, userAgent, archiveMedia),
            statsActor,
            context
          )
        )
      )
      .onFailure(SupervisorStrategy.restart)

}
