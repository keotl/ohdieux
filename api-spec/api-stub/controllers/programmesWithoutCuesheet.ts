import { Controller, Get, Path, Route } from "tsoa";
import {
  ContentType,
  EpisodeId,
  FormattedFileSize,
  MediaId,
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
  ): Promise<ProgrammeWithoutCuesheet> {
    throw new Error();
  }
}

export type Duration = {
  durationInSeconds: number;
};

export type ProgrammeWithoutCuesheet = {
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
          contentType: ContentType;
          id: EpisodeId;
        };
        media2: {
          context: {
            contentType: ContentType;
            id: ProgrammeId;
          };
          details: string;
          download: {
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
          id: MediaId;

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
        summary: string;
        title: string;
        url: string;
      }[];
    };
  };
};
