/**
 * Shared LessonPlan contract.
 *
 * Used by: Teacher Agent (Team 2), Frontend (Team 5), Backend (Team 6).
 */

export interface LessonSegment {
  id: string;
  concept: string;
  minutes: number;
  explanation: string;
  example: string;
  visual_type: "equation" | "diagram" | "graph" | "timeline" | "code" | "none";
  checkpoint: boolean;
}

export interface LessonPlan {
  title: string;
  duration_minutes: number;
  language: string;
  learner_level: "beginner" | "intermediate" | "advanced";
  segments: LessonSegment[];
}

export interface SessionCreate {
  topic?: string;
  document_id?: string;
  language: string;
  learner_level: string;
  duration_minutes: number;
  goal?: string;
}

export interface SessionResponse {
  id: string;
  topic: string | null;
  document_id: string | null;
  language: string;
  learner_level: string;
  duration_minutes: number;
  status: string;
  lesson_plan: LessonPlan | null;
  lesson_state: Record<string, unknown> | null;
}

export interface SessionStartResponse {
  session_id: string;
  lesson_plan: LessonPlan;
  first_segment: LessonSegment | null;
  message: string;
}
