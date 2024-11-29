package ca.ligature.ohdieux.actors.scraper.programme

import ca.ligature.ohdieux.ohdio.RCModels
import ca.ligature.ohdieux.ohdio.RCModels.FetchResult
import scala.collection.immutable.LinearSeq
import ca.ligature.ohdieux.ohdio.RCModels.ProgrammeContentDetailItem

private class EpisodeIterator(
    firstPage: RCModels.ProgrammeById,
    fetcher: (pageNumber: Int) => FetchResult[RCModels.ProgrammeById],
    direction: "normal" | "reverse"
) extends Iterator[RCModels.ProgrammeContentDetailItem] {

  private val totalItems =
    firstPage.content.contentDetail.pagedConfiguration.totalNumberOfItems
  private var currentPage =
    if (direction == "normal") then 1
    else
      (totalItems.toDouble / firstPage.content.contentDetail.pagedConfiguration.pageMaxLength).ceil.toInt

  private var currentPageItems = firstPage.content.contentDetail.items
  if (direction == "reverse") {
    currentPageItems = currentPageItems.reverse
  }

  if (
    currentPage != firstPage.content.contentDetail.pagedConfiguration.pageNumber
  ) {
    fetchCurrentPage()
  }

  private val pageIncrement = if (direction == "normal") then 1 else -1

  override def hasNext: Boolean =
    currentPageItems.headOption.nonEmpty

  override def next(): ProgrammeContentDetailItem = {
    val nextItem =
      currentPageItems.headOption.getOrElse(throw new NoSuchElementException())
    advance()
    nextItem
  }

  private def advance(): Unit = {
    currentPageItems match {
      case Nil => ()
      case x :: Nil => {
        currentPage = currentPage + pageIncrement
        fetchCurrentPage()
      }
      case (x :: xs) => currentPageItems = xs
    }
  }

  private def fetchCurrentPage(): Unit = {
    fetcher(currentPage) match {
      case FetchResult.Success(page) => {
        currentPageItems = page.content.contentDetail.items
        if (direction == "reverse") {
          currentPageItems = currentPageItems.reverse
        }
      }
      case FetchResult.ParseFailure(message) => {
        println(s"ParseFailure ${message}")
        currentPageItems = Nil
      }
      case FetchResult.FetchFailure(message) => {
        println(s"FetchFailure ${message}")
        currentPageItems = Nil
      }
    }
  }
}

object EpisodeIterator {
  def apply(
      firstPage: RCModels.ProgrammeById,
      fetcher: (pageNumber: Int) => FetchResult[RCModels.ProgrammeById]
  ): EpisodeIterator = {
    val ordering = inferProgrammeOrdering(firstPage)

    new EpisodeIterator(
      firstPage,
      fetcher,
      if (ordering == "oldest_to_newest") then ("reverse") else ("normal")
    )
  }

  private def inferProgrammeOrdering(
      firstPage: RCModels.ProgrammeById
  ): "oldest_to_newest" | "newest_to_oldest" | "unknown" = {
    var lastDate = firstPage.content.contentDetail.items
      .find(e => !e.isBroadcastedReplay)
      .get
      .broadcastedFirstTimeAt
    var delta = 0
    for (elem <- firstPage.content.contentDetail.items) do {
      if (!elem.isBroadcastedReplay) {
        if (elem.broadcastedFirstTimeAt.isAfter(lastDate)) {
          delta += 1
        } else if (elem.broadcastedFirstTimeAt.isBefore(lastDate)) {
          delta -= 1
        }
        lastDate = elem.broadcastedFirstTimeAt
      }
    }
    if (delta > 2) {
      "oldest_to_newest"
    } else if (delta < -2) {
      "newest_to_oldest"
    } else {
      "unknown"
    }
  }
}
