/**
 * Shared VideoResult contract.
 *
 * Used by: Video (Team 4), Frontend (Team 5), Backend (Team 6).
 */

export interface VideoResult {
  segment_id: string;
  status: "pending" | "generating" | "completed" | "failed" | "placeholder";
  video_url: string;
  duration_seconds: number;
  language: string;
}

export interface VideoGenerateRequest {
  session_id: string;
  segment_id: string;
  script: string;
  visual_type: string;
  language: string;
}

export interface VideoStatusResponse {
  segment_id: string;
  status: string;
  video_url: string | null;
  duration_seconds: number | null;
}
