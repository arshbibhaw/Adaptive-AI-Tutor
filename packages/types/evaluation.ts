/**
 * Shared StudentEvaluation contract.
 *
 * Used by: Assessment (Team 3), Teacher Agent (Team 2), Frontend (Team 5).
 */

export interface StudentEvaluation {
  question_id: string;
  correct: boolean;
  score: number;
  concept: string;
  misconception: string | null;
  confidence: number;
  next_action: string;
  difficulty: "easy" | "medium" | "hard";
}

export interface AnswerSubmission {
  question_id: string;
  answer: string;
  concept?: string;
}

export interface AnswerResponse {
  evaluation: StudentEvaluation;
  feedback: string;
  next_question: QuestionGenerated | null;
  adaptation: AdaptationResult | null;
}

export interface QuestionGenerated {
  id: string;
  question_text: string;
  question_type: "mcq" | "short_answer" | "conceptual" | "numerical" | "explain";
  concept: string;
  difficulty: string;
  options: string[] | null;
  correct_answer: string | null;
  language: string;
}

export interface AdaptationResult {
  action: string;
  difficulty: string;
  reason: string;
}
