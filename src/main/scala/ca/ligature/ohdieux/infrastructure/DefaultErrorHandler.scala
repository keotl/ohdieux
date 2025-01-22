package ca.ligature.ohdieux.infrastructure
import javax.inject.Singleton

import scala.concurrent._

import play.api.http.HttpErrorHandler
import play.api.mvc._
import play.api.mvc.Results._
import javax.inject.Inject
import play.api.Logger

@Singleton
class DefaultErrorHandler extends HttpErrorHandler {
  val logger: Logger = Logger(this.getClass())

  def onClientError(
      request: RequestHeader,
      statusCode: Int,
      message: String
  ): Future[Result] = {

    if (statusCode == 404) {
      return Future.successful(
        Status(statusCode)("not found")
      )
    }
    logger.error(s"Client error: ${message}")
    Future.successful(
      Status(statusCode)("an error occurred")
    )
  }

  def onServerError(
      request: RequestHeader,
      exception: Throwable
  ): Future[Result] = {
    logger.error(s"Uncaught exception: ${exception.getMessage}")
    Future.successful(
      InternalServerError("error")
    )
  }
}
