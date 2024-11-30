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
                  "01278be1ca37eec8570a3c6341c475c8b5799d571f407f3a9c1a3e2703cc5cc1"
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
                  "a6d745162f4b6d9011e53382fcf981c09968d77909391b9c0e5302853f852444"
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
                  "6674354438ac2a4e609b3f16572a1ef58404fe1f13143e2607860bd1816714c6"
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
                  "3d47cc0b96f17510696f3d4cc180a76cb2bdfb6a9a5dfefe958406687489c72f"
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
      .map(replaceTitle(programmeTitle.toString))

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
