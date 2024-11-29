package ca.ligature.ohdieux

import play.api.libs.json.Reads
import play.api.libs.json.Json
import play.api.libs.json.JsValue
import play.api.libs.json.JsPath
import play.api.libs.json.Writes
import play.api.libs.json.JsString
import java.time.ZonedDateTime

object Models {
  case class ProgrammeDescriptor(
      title: String,
      description: String,
      author: String,
      link: String,
      image_url: String
  )
  case class EpisodeDescriptor(
      title: String,
      description: String,
      guid: String,
      date: ZonedDateTime,
      duration: Int,
      media: List[MediaDescriptor],
      is_broadcast_replay: Boolean
  )

  case class MediaDescriptor(media_url: String, media_type: String, length: Int)

  case class Programme(
      programme_id: Int,
      episodes: List[EpisodeDescriptor],
      build_date: ZonedDateTime
  )

  // JSON Serialization
  implicit val programmeReads: Reads[Programme] = Json.reads[Programme]
  implicit val programmeDescriptorReads: Reads[ProgrammeDescriptor] =
    Json.reads[ProgrammeDescriptor]
  implicit val episodeDescriptorReads: Reads[EpisodeDescriptor] =
    Json.reads[EpisodeDescriptor]
  implicit val mediaDescriptorReads: Reads[MediaDescriptor] =
    Json.reads[MediaDescriptor]
  implicit val episodeOrderingReads: Reads[EpisodeOrdering] =
    (JsPath).read[String].map(EpisodeOrdering.valueOf(_))

  implicit val programmeWrites: Writes[Programme] = Json.writes[Programme]
  implicit val programmeDescriptorWrites: Writes[ProgrammeDescriptor] =
    Json.writes[ProgrammeDescriptor]
  implicit val episodeDescriptorWrites: Writes[EpisodeDescriptor] =
    Json.writes[EpisodeDescriptor]
  implicit val mediaDescriptorWrites: Writes[MediaDescriptor] =
    Json.writes[MediaDescriptor]
  implicit val episodeOrderingWrites: Writes[EpisodeOrdering] =
    new Writes[EpisodeOrdering] {
      def writes(e: EpisodeOrdering) = JsString(e.toString())
    }

}
