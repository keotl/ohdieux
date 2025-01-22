package ca.ligature.ohdieux.infrastructure

import javax.inject._

import org.apache.pekko.actor.ActorSystem
import play.api.libs.concurrent.CustomExecutionContext

@Singleton
class DatabaseExecutionContext @Inject() (system: ActorSystem)
    extends CustomExecutionContext(system, "database.dispatcher")
