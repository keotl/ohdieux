package ca.ligature.ohdieux.actors.config

import org.apache.pekko.actor.typed.scaladsl.ActorContext
import org.apache.pekko.actor.typed.scaladsl.AbstractBehavior
import org.apache.pekko.actor.typed.Behavior
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import ca.ligature.ohdieux.persistence.ProgrammeConfigStatus
import ca.ligature.ohdieux.persistence.ProgrammeConfigRepository
import ca.ligature.ohdieux.persistence.ProgrammeConfigEntity
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

class ProgrammeConfigActor(
    programmeConfigRepository: ProgrammeConfigRepository,
    context: ActorContext[ProgrammeConfigActor.Message]
) extends AbstractBehavior[ProgrammeConfigActor.Message](context) {
  import ProgrammeConfigActor._

  override def onMessage(msg: Message): Behavior[Message] = {
    msg match {
      case Message.SetProgrammeStatus(programmeId, status, message) => {
        programmeConfigRepository.saveProgrammeConfig(
          ProgrammeConfigEntity(
            programmeId,
            status,
            message,
            ZonedDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME)
          )
        )
      }
    }
    this
  }
}

object ProgrammeConfigActor {
  enum Message {
    case SetProgrammeStatus(
        programmeId: Int,
        status: ProgrammeConfigStatus,
        message: String
    );
  }

  def apply(
      programmeConfigRepository: ProgrammeConfigRepository
  ): Behavior[Message] =
    Behaviors.setup(context =>
      new ProgrammeConfigActor(programmeConfigRepository, context)
    )

}
