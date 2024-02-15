import { Controller, Get, Path, Route, Query } from "tsoa";
import {
  ContentType,
  EpisodeId,
  FormattedFileSize,
  MediaId,
  Pagination,
  ProgrammeId,
  QualifiedEpisodeId,
} from "./types";

@Route(
  "/neuro/sphere/v1/audio/apps/products/programmes-without-cuesheet-v2/{programmeId}",
)
export class ProgrammesWithoutCuesheetController extends Controller {
  @Get("{pageNumber}")
  public getProgrammeWithoutCuesheet(
    @Path() programmeId: string,
    @Path() pageNumber: number,
    @Query() context: "web",
  ): Promise<ProgrammeWithoutCuesheet> {
    throw new Error();
  }
}

export type Duration = {
  durationInSeconds: number;
};

export type ProgrammeWithoutCuesheet = {
  canonicalUrl: string;
  header: {
    title: string;
    summary: string;
    picture: {
      url: string;
    };
  };
  content: {
    contentDetail: {
      pagedConfiguration: Pagination;
      items: {
        broadcastedFirstTimeAt: Date;
        duration: Duration;
        globalId: {
          contentType: ContentType;
          id: EpisodeId;
        };
        media2: {
          context: {
            contentType: ContentType;
            id: ProgrammeId;
          };
          details?: string;
          download?: {
            fileSizeInBytes: number;

            /** Undefined if episode is composed of multiple audio files */
            url?: string;
            mediaId?: MediaId;
            formattedFileSize?: FormattedFileSize;
          };
          duration: Duration;
          globalId: {
            contentType: ContentType;
            id: EpisodeId;
          };

          title: string;
        };
        playlistItemId: {
          globalId: QualifiedEpisodeId;
          globalId2: {
            contentType: ContentType;
            id: EpisodeId;
          };
          hasTranscription: boolean;
          /** undefined if episode is composed of multiple audio files */
          mediaId?: MediaId;
          title: string;
        };
        summary: string | undefined;
        title: string;
        url: string;
      }[];
    };
  };
};
