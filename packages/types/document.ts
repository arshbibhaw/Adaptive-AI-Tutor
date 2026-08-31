/**
 * Shared Document types.
 */

export interface DocumentUploadResponse {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: string;
}

export interface DocumentOutlineResponse {
  id: string;
  filename: string;
  outline: DocumentOutline | null;
  status: string;
  chunk_count: number | null;
}

export interface DocumentOutline {
  title: string;
  sections: DocumentSection[];
  total_pages: number;
}

export interface DocumentSection {
  heading: string;
  page: number | null;
}

export interface RetrievalChunk {
  text: string;
  page: number | null;
  chapter: string;
  section: string;
  chunk_id: string;
  score: number;
}
