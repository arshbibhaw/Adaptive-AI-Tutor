/**
 * Shared Learner types.
 */

export interface LearnerProfile {
  id: string;
  user_id: string;
  level: "beginner" | "intermediate" | "advanced";
  language: string;
  goals: string | null;
  preferences: Record<string, unknown> | null;
  strong_concepts: string[];
  weak_concepts: string[];
  learning_history: unknown[];
}

export interface LearnerProfileCreate {
  level: string;
  language: string;
  goals?: string;
  preferences?: Record<string, unknown>;
}

export interface ProgressResponse {
  topic: string;
  concept: string | null;
  mastery: number;
  attempts: number;
  correct_count: number;
  misconceptions: string[];
  status: string;
}

export interface LearningReportResponse {
  session_id: string;
  total_questions: number;
  correct_answers: number;
  score: number;
  strong_concepts: string[];
  weak_concepts: string[];
  misconceptions: string[];
  revision_recommendations: string[];
  next_topic: string | null;
}

export interface OverallProgressResponse {
  user_id: string;
  topics_studied: string[];
  total_sessions: number;
  average_score: number;
  strong_concepts: string[];
  weak_concepts: string[];
  current_learning_path: string[];
}
