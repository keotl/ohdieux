import { Controller, Get, Path, Query, Route } from "tsoa";
import { MediaId, QualifiedEpisodeId } from "./types";

@Route("/neuro/sphere/v1/medias/apps/playback-lists/{playlistItemId}")
export class PlaybackListsController extends Controller {
  @Get()
  public getPlaylistItem(
    @Path() playlistItemId: QualifiedEpisodeId,
    @Query() context: "web",
    @Query() globalId: QualifiedEpisodeId,
  ): Promise<PlaylistItem> {
    throw new Error();
  }
}

type PlaylistItem = {
  items: {
    playlistItemId: {
      mediaId: MediaId;
    };
  }[];
};
