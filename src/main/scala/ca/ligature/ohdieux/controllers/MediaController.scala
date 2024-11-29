package ca.ligature.ohdieux.controllers

import javax.inject.Inject
import play.api.mvc.ControllerComponents
import play.api.mvc.BaseController
import org.apache.pekko.actor.typed.delivery.internal.ProducerControllerImpl.Request
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import java.io.File
import scala.concurrent.ExecutionContext
import java.nio.file.Files
import play.api.mvc.ResponseHeader
import org.apache.pekko.stream.scaladsl.FileIO
import org.apache.pekko.stream.scaladsl.Source
import org.apache.pekko.util.ByteString
import play.api.http.HttpEntity
import play.api.mvc.Result

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
    val mediaHandle = archive.createMediaHandle(media_id)
    if (!archive.exists(mediaHandle)) {
      NotFound("not cached")
    } else {
      val path = archive.getPath(mediaHandle)
      val source: Source[ByteString, ?] = FileIO.fromPath(path)
      val contentLength = Some(Files.size(path))
      Result(
        header = ResponseHeader(200, Map.empty),
        body = HttpEntity.Streamed(source, contentLength, Some("audio/mpeg"))
      )
    }
  }
}
