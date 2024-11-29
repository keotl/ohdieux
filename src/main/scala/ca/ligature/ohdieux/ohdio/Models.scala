package ca.ligature.ohdieux.ohdio

import play.api.libs.json.Json
import play.api.libs.json.Reads
import scala.collection.immutable.LinearSeq
import java.time.ZonedDateTime

object RCModels {
  case class ProgrammeById(
      typename: String,
      canonicalUrl: String,
      content: ProgrammeContent,
      header: ProgrammeHeader
  )

  case class ProgrammeContent(
      typename: String,
      contentDetail: ProgrammeContentDetail,
      id: Int
  )

  case class ProgrammeHeader(
      typename: String,
      title: String,
      summary: String,
      picture: ProgrammePicture
  )

  case class ProgrammePicture(pattern: String)

  case class ProgrammeContentDetail(
      typename: String,
      items: LinearSeq[ProgrammeContentDetailItem],
      pagedConfiguration: PagedConfiguration
  )

  case class ProgrammeContentDetailItem(
      typename: String,
      broadcastedFirstTimeAt: ZonedDateTime,
      duration: Duration,
      isBroadcastedReplay: Boolean,
      playlistItemId: PlaylistItemId,
      summary: String = "",
      title: String,
      url: String
  )

  case class PagedConfiguration(
      pageMaxLength: Int,
      pageNumber: Int,
      pageSize: Int,
      totalNumberOfItems: Int
  )

  case class Duration(durationInSeconds: Int)
  case class PlaylistItemId(
      mediaId: Option[String],
      globalId2: PlaylistItemIdGlobalId2
  )
  case class PlaylistItemIdGlobalId2(
      id: String,
      contentType: PlaylistItemContentType
  )
  case class PlaylistItemContentType(id: Int)

  implicit val programmeByIdReads: Reads[ProgrammeById] =
    Json.reads[ProgrammeById]
  implicit val programmeHeaderReads: Reads[ProgrammeHeader] =
    Json.reads[ProgrammeHeader]
  implicit val programmePictureReads: Reads[ProgrammePicture] =
    Json.reads[ProgrammePicture]
  implicit val programmeContentReads: Reads[ProgrammeContent] =
    Json.reads[ProgrammeContent]
  implicit val programmeContentDetailReads: Reads[ProgrammeContentDetail] =
    Json.reads[ProgrammeContentDetail]
  implicit val programmeContentDetailItemReads
      : Reads[ProgrammeContentDetailItem] =
    Json.reads[ProgrammeContentDetailItem]
  implicit val durationReads: Reads[Duration] = Json.reads[Duration]
  implicit val pagedConfigurationReads: Reads[PagedConfiguration] =
    Json.reads[PagedConfiguration]
  implicit val playlistItemIdReads: Reads[PlaylistItemId] =
    Json.reads[PlaylistItemId]
  implicit val playlistItemIdGlobalId2Reads: Reads[PlaylistItemIdGlobalId2] =
    Json.reads[PlaylistItemIdGlobalId2]
  implicit val playlistItemContentTypeReads: Reads[PlaylistItemContentType] =
    Json.reads[PlaylistItemContentType]

  case class PlaybackListById(typename: String, items: Seq[PlaybackListItem])
  case class PlaybackListItem(
      typename: String,
      appCode: String,
      audioType: String,
      duration: Duration,
      mediaPlaybackItem: MediaPlaybackItem,
      broadcastedFirstTimeAt: ZonedDateTime
  )
  case class MediaPlaybackItem(
      mediaId: String,
      globalId: PlaylistItemIdGlobalId2
  )

  implicit val playbackListByIdReads: Reads[PlaybackListById] =
    Json.reads[PlaybackListById]
  implicit val playbackListItemReads: Reads[PlaybackListItem] =
    Json.reads[PlaybackListItem]
  implicit val mediaPlaybackItemReads: Reads[MediaPlaybackItem] =
    Json.reads[MediaPlaybackItem]

  case class MediaStream(url: String)
  implicit val mediaStreamReads: Reads[MediaStream] = Json.reads[MediaStream]

  enum FetchResult[T] {
    case Success(value: T);
    case FetchFailure(message: String);
    case ParseFailure(message: String);

    def isSuccess: Boolean =
      this match {
        case Success(_) => true
        case _          => false
      }

    def get: T =
      this match {
        case Success(v)      => v
        case FetchFailure(m) => throw new Exception(s"Fetch failure ${m}")
        case ParseFailure(m) => throw new Exception(s"Parse failure ${m}")
      }

    def opt: Option[T] =
      this match {
        case Success(v) => Some(v)
        case _          => None
      }
  }
}
