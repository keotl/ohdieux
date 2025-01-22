package ca.ligature.ohdieux.ohdio

import scala.concurrent.Future
import sttp.client4.quick.*
import play.api.libs.json._
import ca.ligature.ohdieux.persistence.ProgrammeType
import ca.ligature.ohdieux.utils.|>
import play.api.Logger

case class ApiClient(val baseUrl: String, val userAgent: String) {
  import ApiClient._
  import RCModels._
  import RCModels.FetchResult._

  val logger = Logger(this.getClass.getName)

  logger.info(
    s"Initialized ApiClient to ${baseUrl} with User-Agent \"${userAgent}\""
  )

  def getProgrammeById(
      programmeType: ProgrammeType,
      programmeId: Int,
      pageNumber: Int
  ): FetchResult[ProgrammeById] = {
    logger.info(
      s"getProgrammeById(${programmeType}/${programmeId},${pageNumber})"
    )
    if (pageNumber < 1) {
      return FetchFailure("Cannot lookup page below 1.")
    }
    val queryBuilder =
      Queries.buildGetProgrammeByIdQuery(programmeType, programmeId, pageNumber)

    if (queryBuilder.isEmpty) {
      return FetchFailure("No query to send")
    }

    val (queryParams, transform) = queryBuilder.get
    val response = quickRequest
      .get(uri"$baseUrl/bff/audio/graphql?$queryParams")
      .header("User-Agent", userAgent)
      .header("Content-Type", "application/json")
      .send()

    if (!response.code.isSuccess) {
      return FetchFailure(s"Request failed with ${response.code.code}")
    }

    val body = Json.parse(response.body) |> transform

    val decoded =
      (body \ "data" \ "programmeById").validate[ProgrammeById]

    decoded.map(Success(_)).getOrElse(ParseFailure(_1))
  }

  def getPlaybacklistById(
      contentTypeId: Int,
      playbackListId: String
  ): FetchResult[PlaybackListById] = {
    logger.info(s"getPlaybackListById(${contentTypeId}, ${playbackListId})")
    if (playbackListId.toInt < 0) {
      return FetchFailure(s"Refusing getPlaybackListById with negative id.")
    }
    val query =
      Queries.buildGetPlaybackListByGlobalIdQuery(contentTypeId, playbackListId)

    val response = quickRequest
      .get(uri"$baseUrl/bff/audio/graphql?$query")
      .header("User-Agent", userAgent)
      .header("Content-Type", "application/json")
      .send()

    if (!response.code.isSuccess) {
      return FetchFailure(s"Request failed with ${response.code.code}")
    }

    val body = Json.parse(response.body)

    val decoded =
      (body \ "data" \ "playbackListByGlobalId").validate[PlaybackListById]

    decoded.map(Success(_)).getOrElse(ParseFailure(_1))
  }

  def getMedia(
      mediaId: Int,
      tech: "hls" | "progressive"
  ): FetchResult[MediaStream] = {
    logger.info(s"getMedia(${mediaId}, ${tech})")
    val query = Map(
      "appCode" -> "medianet",
      "connectionType" -> "hd",
      "deviceType" -> "ipad",
      "idMedia" -> mediaId,
      "multibitrate" -> "true",
      "output" -> "json",
      "tech" -> tech
    )

    val response = quickRequest
      .get(uri"$baseUrl/media/validation/v2?$query")
      .header("User-Agent", userAgent)
      .header("Content-Type", "application/json")
      .send()

    if (!response.code.isSuccess) {
      return FetchFailure(s"Request failed with ${response.code.code}")
    }

    val body = Json.parse(response.body)

    val decoded =
      (body).validate[MediaStream]

    decoded.map(Success(_)).getOrElse(ParseFailure(_1))
  }

}
