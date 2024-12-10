import com.google.inject.AbstractModule
import org.apache.pekko.actor.typed.ActorRef
import play.api.libs.concurrent.PekkoGuiceSupport
import ca.ligature.ohdieux.persistence._
import ca.ligature.ohdieux.persistence.impl._
import ca.ligature.ohdieux.ohdio.ApiClient
import ca.ligature.ohdieux.actors.scraper.media.MediaScraperActor

import play.api.Configuration
import play.api.Environment
import ca.ligature.ohdieux.actors.scraper.programme.ProgrammeScraperActor
import com.google.inject.Provides
import com.google.inject.Singleton
import org.apache.pekko.actor.typed.ActorSystem
import ca.ligature.ohdieux.actors.file.impl.ArchivedFileRepository
import ca.ligature.ohdieux.actors.file.FileArchiveActor
import ca.ligature.ohdieux.services.manifest.ManifestService
import ca.ligature.ohdieux.services.manifest.types.ManifestRenderServerOptions
import ca.ligature.ohdieux.infrastructure.DefaultErrorHandler
import scala.collection.immutable.HashSet
import ca.ligature.ohdieux.actors.stats.ArchiveStatisticsActor

class Module(environment: Environment, configuration: Configuration)
    extends AbstractModule
    with PekkoGuiceSupport {

  override def configure() = {
    bind(classOf[ProgrammeRepository]).to(classOf[DatabaseProgrammeRepository])
    bind(classOf[DatabaseProgrammeRepository])
    bind(classOf[EpisodeRepository]).to(classOf[DatabaseEpisodeRepository])
    bind(classOf[MediaRepository]).to(classOf[DatabaseMediaRepository])
    bind(classOf[ManifestService])
    bind(classOf[ManifestRepository]).to(
      classOf[DatabaseProgrammeManifestRepository]
    )
    bind(classOf[StatisticsRepository]).to(
      classOf[DatabaseStatisticsRepository]
    )
    bind(classOf[ProgrammeConfigRepository]).to(
      classOf[DatabaseProgrammeConfigRepository]
    )
    bind(classOf[ArchivedFileRepository]).toInstance(
      new ArchivedFileRepository(
        configuration.get("archive.base_dir"),
        configuration.get("archive.temp_dir")
      )
    )
    bind(classOf[DefaultErrorHandler])

    bind(classOf[ApiClient]).toInstance(
      new ApiClient(
        configuration.get("rc.base_url"),
        configuration.get("rc.user_agent")
      )
    )
    bind(classOf[ManifestRenderServerOptions]).toInstance(
      ManifestRenderServerOptions(
        serveArchivedImages = configuration.get("manifest.serve_images"),
        imageArchiveBaseUrl =
          configuration.get("manifest.image_archive_base_url"),
        serveArchivedMedia = configuration.get("manifest.serve_media"),
        mediaArchiveBaseUrl =
          configuration.get("manifest.media_archive_base_url"),
        autoAddProgrammes = configuration.get("scraper.auto_add_programmes")
      )
    )
  }

  @Provides @Singleton
  def provideMediaScraperActor(
      apiClient: ApiClient,
      mediaRepository: MediaRepository,
      episodeRepository: EpisodeRepository,
      fileArchiver: ActorRef[FileArchiveActor.Message],
      archive: ArchivedFileRepository,
      config: Configuration
  ): ActorRef[MediaScraperActor.Message] = {
    return ActorSystem[MediaScraperActor.Message](
      MediaScraperActor(
        apiClient,
        mediaRepository,
        episodeRepository,
        fileArchiver,
        archive,
        config.get("archive.archive_media"),
        HashSet() ++ config.get[Seq[Int]]("archive.programme_blacklist")
      ),
      "media-scraper"
    )
  }

  @Provides @Singleton
  def provideProgrammeScraperActor(
      apiClient: ApiClient,
      programmeRepository: ProgrammeRepository,
      episodeRepository: EpisodeRepository,
      programmeConfigRepository: ProgrammeConfigRepository,
      mediaScraperRef: ActorRef[MediaScraperActor.Message],
      archiveRef: ActorRef[FileArchiveActor.Message],
      config: Configuration
  ): ActorRef[ProgrammeScraperActor.Message] = {
    return ActorSystem[ProgrammeScraperActor.Message](
      ProgrammeScraperActor(
        apiClient,
        programmeRepository,
        episodeRepository,
        programmeConfigRepository,
        config.get("scraper.max_episodes"),
        mediaScraperRef,
        archiveRef,
        config.get("scraper.refresh_interval")
      ),
      "programme-scraper"
    )
  }

  @Provides @Singleton
  def provideFileArchiveActor(
      statsActor: ActorRef[ArchiveStatisticsActor.Message],
      archive: ArchivedFileRepository,
      config: Configuration
  ): ActorRef[FileArchiveActor.Message] = {
    return ActorSystem[FileArchiveActor.Message](
      FileArchiveActor(
        statsActor,
        archive,
        config.get("rc.user_agent"),
        config.get("archive.archive_media")
      ),
      "file-archive"
    )
  }

  @Provides @Singleton
  def provideArchiveStatisticsActor(
      manifestRepository: ManifestRepository,
      statsRepository: StatisticsRepository,
      archive: ArchivedFileRepository
  ): ActorRef[ArchiveStatisticsActor.Message] = {
    return ActorSystem[ArchiveStatisticsActor.Message](
      ArchiveStatisticsActor(
        manifestRepository,
        statsRepository,
        archive
      ),
      "archive-stats"
    )
  }
}
