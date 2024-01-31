import { Controller, Get, Query, Route } from "tsoa";
import { MediaId } from "./types";

@Route("/media/validation/v2/")
export class MediaController extends Controller {
  @Get()
  public getMediaStream(
    @Query() appCode: "medianet",
    @Query() connectionType: "hd",
    @Query() deviceType: "ipad",
    @Query() idMedia: MediaId,
    @Query() multibitrate: "true",
    @Query() output: "json",
    @Query() tech: StreamingTech,
  ): Promise<MediaStreamDescriptor> {
    throw new Error();
  }
}

type StreamingTech = "progressive" | "hls";
export type MediaStreamDescriptor = {
  url: string;
};
