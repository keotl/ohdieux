package ca.ligature.ohdieux.ohdio

import play.api.libs.json._
import ca.ligature.ohdieux.persistence.ProgrammeType

private object Queries {
  import ApiClient._
  import RCModels._
  import RCModels.FetchResult._

  def buildGetPlaybackListByGlobalIdQuery(
      contentTypeId: Int,
      playbackListId: String
  ): Map[String, String] = {
    Map(
      "opname" -> "playbackListByGlobalId",
      "extensions" -> Json.stringify(
        JsObject(
          Seq(
            "persistedQuery" -> JsObject(
              Seq(
                "version" -> JsNumber(1),
                "sha256Hash" -> JsString(
                  "ae95ebffe69f06d85a0f287931b61e3b7bfb7485f28d4d906c376be5f830b8c0"
                )
              )
            )
          )
        )
      ),
      "variables" -> Json.stringify(
        JsObject(
          Seq(
            "params" -> JsObject(
              Seq(
                "contentTypeId" -> JsNumber(contentTypeId),
                "id" -> JsString(playbackListId)
              )
            )
          )
        )
      )
    )
  }

  def buildGetProgrammeByIdQuery(
      programmeType: ProgrammeType,
      programmeId: Int,
      pageNumber: Int
  ): Option[(Map[String, String], JsValue => JsValue)] =
    programmeType match {
      case ProgrammeType.Balado => {
        val extensions = JsObject(
          Seq(
            "persistedQuery" -> JsObject(
              Seq(
                "version" -> JsNumber(1),
                "sha256Hash" -> JsString(
                  "3cf8cb9c41eea3f2a8e0e34a32dd38be14dc653620df59d19b0ddc0dbf5bd0df"
                )
              )
            )
          )
        )

        val variables = JsObject(
          Seq(
            "params" -> JsObject(
              Seq(
                "context" -> JsString("web"),
                "forceWithoutCueSheet" -> JsBoolean(true),
                "id" -> JsNumber(programmeId),
                "pageNumber" -> JsNumber(pageNumber)
              )
            )
          )
        )

        return Some(
          Map(
            "opname" -> "programmeById",
            "extensions" -> Json.stringify(extensions),
            "variables" -> Json.stringify(variables)
          ),
          identity
        )
      }

      case ProgrammeType.EmissionPremiere => {
        val extensions = JsObject(
          Seq(
            "persistedQuery" -> JsObject(
              Seq(
                "version" -> JsNumber(1),
                "sha256Hash" -> JsString(
                  "43140230d24ccd46d04ac08d9a413d7f94b4bfc0f3145ee926b12de377f64335"
                )
              )
            )
          )
        )

        val variables = JsObject(
          Seq(
            "params" -> JsObject(
              Seq(
                "context" -> JsString("web"),
                "forceWithoutCueSheet" -> JsBoolean(false),
                "id" -> JsNumber(programmeId),
                "pageNumber" -> JsNumber(pageNumber)
              )
            )
          )
        )

        return Some(
          Map(
            "opname" -> "programmeById",
            "extensions" -> Json.stringify(extensions),
            "variables" -> Json.stringify(variables)
          ),
          identity
        )
      }

      case ProgrammeType.GrandeSerie => {
        val extensions = JsObject(
          Seq(
            "persistedQuery" -> JsObject(
              Seq(
                "version" -> JsNumber(1),
                "sha256Hash" -> JsString(
                  "998ab7dcd371db7319c9fe18e027ef971f267e9584c9117afaeeb24e06aae7b6"
                )
              )
            )
          )
        )

        val variables = JsObject(
          Seq(
            "params" -> JsObject(
              Seq(
                "context" -> JsString("web"),
                "forceWithoutCueSheet" -> JsBoolean(true),
                "id" -> JsNumber(programmeId),
                "pageNumber" -> JsNumber(pageNumber)
              )
            )
          )
        )

        return Some(
          Map(
            "opname" -> "programmeById",
            "extensions" -> Json.stringify(extensions),
            "variables" -> Json.stringify(variables)
          ),
          identity
        )
      }

      case ProgrammeType.Audiobook => {
        if (pageNumber > 1) {
          return None
        }
        val extensions = JsObject(
          Seq(
            "persistedQuery" -> JsObject(
              Seq(
                "version" -> JsNumber(1),
                "sha256Hash" -> JsString(
                  "fffa8c9d5062d18637e341f329d6e4d91709ab7cdd3ef87646ef80fa1e05dd29"
                )
              )
            )
          )
        )

        val variables = JsObject(
          Seq(
            "params" -> JsObject(
              Seq(
                "context" -> JsString("web"),
                "id" -> JsNumber(programmeId)
              )
            )
          )
        )

        return Some(
          Map(
            "opname" -> "audioBookById",
            "extensions" -> Json.stringify(extensions),
            "variables" -> Json.stringify(variables)
          ),
          audioBookTransform
        )
      }
    }
}

private def identity[T](x: T): T = x
private def audioBookTransform(x: JsValue): JsValue = {
  val programmeTitle = (x \ "data" \ "audioBookById" \ "header" \ "title")
    .getOrElse(JsString("unknown"))
  val patchedItems =
    (x \ "data" \ "audioBookById" \ "content" \ "contentDetail" \ "items").get
      .asInstanceOf[JsArray]
      .value
      .map(replaceTitle(programmeTitle.as[JsString].value))

  // audiobooks reuse the same episode id. This hack ensures that at
  // least each segment has a relevant title. Otherwise, one random
  // segment tile will be picked as the episode title.
  Json.obj(
    "data" ->
      Json
        .obj("programmeById" -> (x \ "data" \ "audioBookById").get)
        .deepMerge(
          Json.obj(
            "programmeById" -> Json.obj(
              "content" -> Json.obj(
                "contentDetail" -> Json.obj(
                  "items" -> patchedItems,
                  "pagedConfiguration" ->
                    Json.obj(
                      "pageMaxLength" -> 1,
                      "pageNumber" -> 1,
                      "pageSize" -> 25,
                      "totalNumberOfItems" -> patchedItems.length
                    )
                )
              )
            )
          )
        )
  )
}

private def replaceTitle(title: String)(x: JsValue): JsValue = {
  if (!x.isInstanceOf[JsObject]) {
    x
  } else {
    x.as[JsObject] + ("title" -> JsString(title))
  }
}
