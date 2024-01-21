import { Controller, Get, Path, Route } from "tsoa";

@Route(
  "/neuro/sphere/v1/audio/apps/products/programmes-without-cuesheet-v2/{programmeId}",
)
export class ProgrammesWithoutCuesheetController extends Controller {
  @Get("{pageNumber}")
  public getProgrammeWithoutCuesheet(
    @Path() programmeId: string,
    @Path() pageNumber: number,
  ): Promise<ProgrammeWithoutCuesheet> {
    throw new Error();
  }
}

export type Duration = {
  accessibleDuration: string;
  durationInSeconds: number;
  formattedDuration: string;
};

type ProgrammeId = string;
type EpisodeId = string;
type MediaId = string;
type FormattedFileSize = string; // e.g. "10 Mo"
type QualifiedEpisodeId = string; // {contentType}-{episodeId}

export type ProgrammeWithoutCuesheet = {
  // __typename: string;
  canonicalUrl: string;
  content: {
    contentDetail: {
      items: {
        broadcastedFirstTimeAt: Date;
        download: {
          fileSizeInBytes: number;
        };
        duration: Duration;
        globalId: {
          contentType: {
            id: 18;
          };
          id: EpisodeId;
        };
        media2: {
          context: {
            contentType: {
              id: 24;
            };
            id: ProgrammeId;
          };
          details: string;
          download: {
            fileSizeInBytes: number;
            formattedFileSize: FormattedFileSize;
            mediaId: MediaId;
            url: string;
          };
          duration: Duration;
          globalId: {
            contentType: {
              id: 18;
              name: "Épisode";
            };
            id: EpisodeId;
          };
          id: MediaId;

          title: string;
        };
        playlistItemId: {
          globalId: QualifiedEpisodeId;
          globalId2: {
            contentType: {
              id: 18;
              name: "Épisode";
            };
            id: EpisodeId;
          };
          hasTranscription: boolean;
          mediaId: MediaId;
          title: string;
        };
        summary: string;
        title: string;
        url: string;
        $type: "RC.Sphere.Dtos.V1.ContentSummaryCard, RC.Sphere.Dtos";
      }[];
    };
  };
};
