package ca.ligature.ohdieux.services.manifest.render

import org.apache.commons.text.StringEscapeUtils
import ca.ligature.ohdieux.utils.|>

object CleanTextUtils {
  def clean(text: String): String = {
    text
      |> unsafeStripTags
      |> StringEscapeUtils.unescapeHtml4
      |> StringEscapeUtils.escapeXml11
  }

  private def unsafeStripTags(text: String): String =
    TAGS_PATTERN.replaceAllIn(text, "")

  private val TAGS_PATTERN = "<[^<]+?>".r
}
