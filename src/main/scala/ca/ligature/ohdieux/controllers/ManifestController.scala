package ca.ligature.ohdieux.controllers

import javax.inject._
import play.api._
import play.api.mvc._
import ca.ligature.ohdieux.Models
import play.api.libs.json.Json
import scala.concurrent.ExecutionContext
import ca.ligature.ohdieux.persistence.ManifestRepository
import ca.ligature.ohdieux.services.manifest.ManifestService
import ca.ligature.ohdieux.services.manifest.types.ManifestRenderUserOptions

@Singleton
class ManifestController @Inject() (
    val manifestService: ManifestService,
    val controllerComponents: ControllerComponents
)(implicit ec: ExecutionContext)
    extends BaseController {

  def rss(
      programme_id: Int,
      reverse: Option[Boolean],
      tag_segments: Option[Boolean],
      limit_episodes: Option[Boolean],
      exclude_replays: Option[Boolean],
      favor_aac: Option[Boolean]
  ) = Action { implicit request: Request[AnyContent] =>
    val programme = manifestService.renderManifest(
      programme_id,
      ManifestRenderUserOptions(
        reverse = reverse.getOrElse(false),
        tag_segments = tag_segments.getOrElse(false),
        limit_episodes = limit_episodes.getOrElse(false),
        exclude_replays = exclude_replays.getOrElse(false),
        favor_aac = favor_aac.getOrElse(false)
      )
    )

    programme
      .map(p =>
        Ok(views.xml.manifest(p))
          .as("application/xml")
          .withHeaders(
            "Cache-Control" -> "max-age=1800, stale-if-error=86400"
          )
      )
      .getOrElse(NotFound("not found"))
  }
}
