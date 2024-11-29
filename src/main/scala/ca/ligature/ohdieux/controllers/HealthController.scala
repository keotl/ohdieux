package ca.ligature.ohdieux.controllers
import play.api.mvc.BaseController
import play.api.mvc.Request
import play.api.mvc.AnyContent
import javax.inject.Inject
import play.api.mvc.ControllerComponents

class HealthController @Inject() (
    val controllerComponents: ControllerComponents
) extends BaseController {
  def index() = Action { implicit request: Request[AnyContent] =>
    {
      Ok("healthy")
    }
  }
}
