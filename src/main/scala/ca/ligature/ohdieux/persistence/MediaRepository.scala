package ca.ligature.ohdieux.persistence

case class MediaEntity(
    id: Int,
    episode_id: Int,
    episode_index: Int,
    length: Int,
    upstream_url: String
)

trait MediaRepository {
  def getById(id: Int): Option[MediaEntity]
  def getByEpisodeId(episodeId: Int): Seq[MediaEntity]
  def save(entity: MediaEntity): Unit
}
