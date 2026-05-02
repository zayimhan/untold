export interface ArchiveMatch {
  id: string;
  text: string;
  context: string;
  year: number;
  source_type: string;
  similarity: number;
}

export interface TransformResponse {
  lyric: string;
  matches: ArchiveMatch[];
  ambient_track: string;
}
