package ca.ligature.ohdieux.controllers

import javax.inject.Inject
import play.api.mvc.BaseController
import play.api.mvc.Request
import play.api.mvc.AnyContent
import org.apache.pekko.actor.typed.ActorRef
import ca.ligature.ohdieux.actors.scraper.programme.ProgrammeScraperActor
import ca.ligature.ohdieux.actors.scraper.media.MediaScraperActor
import play.api.mvc.ControllerComponents
import ca.ligature.ohdieux.persistence.ProgrammeRepository
import ca.ligature.ohdieux.services.StatisticsService
import ca.ligature.ohdieux.actors.stats.ArchiveStatisticsActor

class AdminController @Inject() (
    val scraper: ActorRef[ProgrammeScraperActor.Message],
    val mediaScraper: ActorRef[MediaScraperActor.Message],
    val archiveStatsActor: ActorRef[ArchiveStatisticsActor.Message],
    val statisticsService: StatisticsService,
    val controllerComponents: ControllerComponents
) extends BaseController {

  def index() = Action { implicit request: Request[AnyContent] =>
    {
      val stats = statisticsService.getGlobalStatistics()

      Ok(views.html.dashboard.index(stats))
    }
  }

  def refresh(programme_id: Int, incremental: Option[Boolean]) = Action {
    implicit request: Request[AnyContent] =>
      {
        scraper.tell(
          ProgrammeScraperActor.Message
            .FetchProgramme(programme_id, incremental.getOrElse(true))
        )
        Ok("ok")
      }
  }
  /*
   * Retrigger missing downloads for every known episode
   */
  def rescanArchive(programme_id: Int) = Action {
    implicit request: Request[AnyContent] =>
      {
        mediaScraper.tell(
          MediaScraperActor.Message
            .RetriggerDownloads(programme_id)
        )
        Ok("ok")
      }
  }

  def recomputeArchiveStatistics() = Action {
    implicit request: Request[AnyContent] =>
      {
        archiveStatsActor.tell(
          ArchiveStatisticsActor.Message.RecomputeArchiveStatistics()
        )
        Ok("ok")
      }
  }
}
