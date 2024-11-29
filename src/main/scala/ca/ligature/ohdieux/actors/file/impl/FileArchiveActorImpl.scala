package ca.ligature.ohdieux.actors.file.impl

case class FileArchiveActorImpl(
    archive: ArchivedFileRepository,
    userAgent: String,
    archiveMedia: Boolean
) {

  def saveImage(programmeId: Int, imageUrl: String): Unit = {
    val savedImage = archive.createImageHandle(programmeId)
    if (!archive.exists(savedImage)) {
      val tempFile = archive.getTemporaryFileHandle(".jpg")
      execProcess("wget", "--user-agent", userAgent, "-O", tempFile, imageUrl)
      archive.moveToArchive(tempFile, savedImage)
    }
  }

  def saveMedia(mediaId: Int, mediaUrl: String, skipDownload: Boolean): Unit = {
    val savedMedia = archive.createMediaHandle(mediaId)
    if (!archive.exists(savedMedia) && archiveMedia && !skipDownload) {
      val tempFile = archive.getTemporaryFileHandle(".mp4")
      execProcess(
        "ffmpeg",
        "-loglevel",
        "error",
        "-user_agent",
        userAgent,
        "-i",
        mediaUrl,
        "-acodec",
        "copy",
        tempFile
      )
      archive.moveToArchive(tempFile, savedMedia)
    }
  }

  private def execProcess(args: String*): Unit = {
    println(s"Executing ${args}")
    val pb = new ProcessBuilder(args*).inheritIO()
    val process = pb.start()

    val exitCode = process.waitFor()
    if (exitCode != 0) {
      throw new Exception(s"Command failed: ${args} ${exitCode}")
    }
  }
}
