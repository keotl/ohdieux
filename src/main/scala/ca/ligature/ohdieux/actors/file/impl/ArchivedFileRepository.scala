package ca.ligature.ohdieux.actors.file.impl

import java.nio.file.Paths
import java.nio.file.Path
import java.io.File
import java.util.UUID
import java.nio.file.Files

private sealed trait ArchiveHandle;
private case class ArchivedImageHandle(programmeId: Int, revision: Int)
    extends ArchiveHandle
private case class ArchivedMediaHandle(mediaId: Int) extends ArchiveHandle

case class ArchivedFileRepository(rootFolder: String, temporaryFolder: String) {

  private val archiveRoot = Paths.get(rootFolder)
  private val imagesFolder = archiveRoot.resolve("images")
  private val mediaFolder = archiveRoot.resolve("media")

  private val tempFolder = Paths.get(temporaryFolder)

  createFolders(Seq(imagesFolder, mediaFolder, tempFolder))

  def getPath(
      archiveHandle: ArchiveHandle
  ): Path = {
    archiveHandle match {
      case ArchivedImageHandle(programmeId, revision) =>
        imagesFolder.resolve(s"${programmeId}.${revision}.jpg")
      case ArchivedMediaHandle(mediaId) =>
        mediaFolder.resolve(s"${mediaId}.mp4")
    }
  }

  def getTemporaryFileHandle(ext: String = ""): String = {
    val uuid = UUID.randomUUID()
    tempFolder.resolve(s"${uuid}${ext}").toString
  }

  def moveToArchive(tempFile: String, destination: ArchiveHandle): Unit = {
    Files.move(Paths.get(tempFile), getPath(destination))
  }

  def createImageHandle(programmeId: Int): ArchivedImageHandle = {
    return ArchivedImageHandle(programmeId, 0)
  }

  def createMediaHandle(mediaId: Int): ArchivedMediaHandle = {
    return ArchivedMediaHandle(mediaId)
  }

  def exists(
      archiveHandle: ArchiveHandle
  ): Boolean = {
    val path = getPath(archiveHandle)
    val file = new File(path.toString)
    file.exists
  }

  private def createFolders(paths: Seq[Path]): Unit = {
    for (path <- paths) do {
      val folder = new File(path.toString())
      if (!folder.exists()) {
        val result = folder.mkdirs()
        if (!result) {
          throw new Exception(s"could not create folder ${path}")
        }
      }
    }
  }

}
