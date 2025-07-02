package ca.ligature.ohdieux.services.manifest.render

import org.apache.commons.text.StringEscapeUtils
import ca.ligature.ohdieux.utils.|>

object CleanTextUtils {
  def clean(text: String): String = {
    text
      |> replaceLineBreaks
      |> unsafeStripTags
      |> StringEscapeUtils.unescapeHtml4
  }

  private def replaceLineBreaks(text: String): String =
    BREAK_PATTERN.replaceAllIn(text, " ")
  private val BREAK_PATTERN = "<br(/)?>".r

  private def unsafeStripTags(text: String): String =
    TAGS_PATTERN.replaceAllIn(text, "")
  private val TAGS_PATTERN = "<[^<]+?>".r

}
