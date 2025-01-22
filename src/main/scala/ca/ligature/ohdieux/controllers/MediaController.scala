package ca.ligature.ohdieux.controllers

import javax.inject.Inject
import play.api.mvc.{
  AnyContent,
  BaseController,
  ControllerComponents,
  RangeResult,
  Request,
  ResponseHeader,
  Result
}
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository

import java.io.File
import scala.concurrent.ExecutionContext
import java.nio.file.Files
import org.apache.pekko.stream.scaladsl.FileIO
import org.apache.pekko.stream.scaladsl.Source
import org.apache.pekko.util.ByteString
import play.api.http.HttpEntity

class MediaController @Inject() (
    archive: ArchivedFileRepository,
    val controllerComponents: ControllerComponents
)(implicit ec: ExecutionContext)
    extends BaseController {

  def getImage(programme_id: Int) = Action {
    val imageHandle = archive.createImageHandle(programme_id)
    if (!archive.exists(imageHandle)) {
      NotFound("")
    } else {
      Ok.sendFile(
        content = new File(archive.getPath(imageHandle).toString),
        fileName = _ => None
      ).as("image/jpeg")
    }
  }

  def getMedia(media_id: Int) = Action {
    implicit request: Request[AnyContent] =>
      {
        val mediaHandle = archive.createMediaHandle(media_id)
        if (!archive.exists(mediaHandle)) {
          NotFound("not cached")
        } else {
          val path = archive.getPath(mediaHandle)
          val source: Source[ByteString, ?] = FileIO.fromPath(path)
          val contentLength = Some(Files.size(path))

          RangeResult.ofSource(
            entityLength = contentLength,
            source = source,
            rangeHeader = request.headers.get(RANGE),
            fileName = Some(s"${media_id}.m4a"),
            contentType = Some("audio/mpeg")
          )
        }
      }
  }
  def getMediaFile(media_file: String) = {
    val media_id = ".m4a$".r.replaceAllIn(media_file, "").toInt
    getMedia(media_id)
  }
}
