package ca.ligature.ohdieux.actors.scraper.programme
import ca.ligature.ohdieux.ohdio.ApiClient
import ca.ligature.ohdieux.ohdio.RCModels.FetchResult.Success
import ca.ligature.ohdieux.persistence.ProgrammeRepository
import ca.ligature.ohdieux.persistence.ProgrammeType
import ca.ligature.ohdieux.persistence.EpisodeRepository
import ca.ligature.ohdieux.ohdio.RCModels
import scala.annotation.tailrec
import ca.ligature.ohdieux.actors.file.FileArchiveActor

private case class ProgrammeScraperActorImpl(
    api: ApiClient,
    programmeRepository: ProgrammeRepository,
    episodeRepository: EpisodeRepository,
    maxDepth: Int,
    onNewEpisode: (
        episode: RCModels.ProgrammeContentDetailItem,
        parentProgrammeId: Int
    ) => Unit,
    onNewProgrammeImage: (programmeId: Int, imageUrl: String) => Unit
) {
  def fetchProgramme(
      programmeId: Int,
      incremental: Boolean
  ): Unit = {
    val savedProgramme = programmeRepository.getById(programmeId)

    val programmeType = savedProgramme
      .map(_.programme_type)
      .orElse(guessProgrammeType(programmeId))

    programmeType match {
      case None =>
        throw new Exception(s"Could not find programmeType for $programmeId")
      case _ => ()
    }

    val fetcher = api.getProgrammeById(programmeType.get, programmeId, _)

    val firstPage = fetcher(1)

    firstPage match {
      case Success(page) =>
        val programme = Assembler.assembleProgramme(page)
        programmeRepository.save(programme)
        onNewProgrammeImage(
          programmeId,
          programme.image_url
        )
        saveEpisodes(
          programmeId,
          EpisodeIterator(page, fetcher),
          incremental,
          1
        )
      case _ => ()
    }
  }

  @tailrec private def saveEpisodes(
      programmeId: Int,
      iterator: EpisodeIterator,
      incremental: Boolean,
      depth: Int
  ): Unit = {
    val episode = iterator.next()
    val savedEpisode =
      episodeRepository.getById(episode.playlistItemId.globalId2.id.toInt)
    episodeRepository.save(Assembler.assembleEpisode(programmeId, episode))

    onNewEpisode(episode, programmeId)

    val exceedsMaxDepth = maxDepth != 0 && depth >= maxDepth

    if (
      iterator.hasNext
      && (!incremental || savedEpisode.isEmpty)
      && !exceedsMaxDepth
    ) {
      saveEpisodes(programmeId, iterator, incremental, depth + 1)
    }
  }

  private def guessProgrammeType(
      programmeId: Int
  ): Option[ProgrammeType] =
    println(s"guessing programme type for $programmeId")
    LazyList(ProgrammeType.values*)
      .map(api.getProgrammeById(_, programmeId, 1))
      .find(_.isSuccess)
      .map(_.get)
      .map(Assembler.guessProgrammeType)

}
