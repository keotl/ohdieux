package ca.ligature.ohdieux.actors.scraper.programme
import ca.ligature.ohdieux.ohdio.RCModels
import ca.ligature.ohdieux.persistence._
import java.time.format.DateTimeFormatter
import java.time.ZonedDateTime

private object Assembler {
  def assembleProgramme(
      programme: RCModels.ProgrammeById
  ): ProgrammeEntity =
    ProgrammeEntity(
      id = programme.content.id,
      programme_type = guessProgrammeType(programme),
      title = programme.header.title,
      description = programme.header.summary,
      author = "Radio-Canada",
      canonical_url =
        "https://ici.radio-canada.ca/ohdio" ++ programme.canonicalUrl,
      image_url = programme.header.picture.pattern
        .replace("{width}", "1400")
        .replace("{ratio}", "1x1"),
      episodes =
        programme.content.contentDetail.pagedConfiguration.totalNumberOfItems,
      last_checked = ZonedDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME)
    )

  def assembleEpisode(
      programmeId: Int,
      programmeItem: RCModels.ProgrammeContentDetailItem
  ): EpisodeEntity =
    EpisodeEntity(
      id = programmeItem.playlistItemId.globalId2.id.toInt,
      title = programmeItem.title,
      description = programmeItem.summary,
      programme_id = programmeId,
      date = programmeItem.broadcastedFirstTimeAt.format(
        DateTimeFormatter.ISO_DATE_TIME
      ),
      duration = programmeItem.duration.durationInSeconds,
      is_broadcast_replay = if (programmeItem.isBroadcastedReplay) 1 else 0
    )

  def guessProgrammeType(
      programme: RCModels.ProgrammeById
  ): ProgrammeType = {
    programme.typename match {
      case "EmissionPremiere"      => ProgrammeType.EmissionPremiere
      case "EmissionBalado"        => ProgrammeType.Balado
      case "EmissionGrandesSeries" => ProgrammeType.GrandeSerie
    }
  }
}
