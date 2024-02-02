export type ProgrammeId = string;
export type EpisodeId = string;
export type MediaId = string;
export type FormattedFileSize = string; // e.g. "10 Mo"
export type QualifiedEpisodeId = string; // {contentType}-{episodeId}

export type ProgrammeEpisode = {
  id: 18;
};
export type Podcast = {
  id: 24;
};
export type ContentType = ProgrammeEpisode | Podcast;

export type Pagination = {
  nextPageUrl: string | null;
  pageMaxLength: number;
  pageNumber: number;
  pageSize: number;
  previousPageUrl: string | null;
  totalNumberOfItems: number;
};
