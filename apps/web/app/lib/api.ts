/**
 * API client for communicating with the AI Teacher backend.
 *
 * All backend calls go through this module.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

/** Helper to get auth headers */
function getHeaders(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const headers: HeadersInit = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

/** Generic fetch wrapper with error handling */
async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: getHeaders(),
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `API error: ${res.status}`);
  }
  return res.json();
}

// --- Auth ---
export async function register(email: string, password: string, full_name?: string) {
  return apiFetch<{ access_token: string }>("/learner/register", {
    method: "POST",
    body: JSON.stringify({ email, password, full_name }),
  });
}

export async function login(email: string, password: string) {
  return apiFetch<{ access_token: string }>("/learner/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

// --- Learner Profile ---
export async function getProfile() {
  return apiFetch("/learner/profile");
}

export async function updateProfile(data: {
  level: string;
  language: string;
  goals?: string;
}) {
  return apiFetch("/learner/profile", {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

// --- Documents ---
export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const headers: HeadersInit = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: "POST",
    headers,
    body: formData,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `Upload failed: ${res.status}`);
  }
  return res.json();
}

export async function indexDocument(documentId: string) {
  return apiFetch(`/documents/${documentId}/index`, { method: "POST" });
}

export async function getDocumentOutline(documentId: string) {
  return apiFetch(`/documents/${documentId}/outline`);
}

// --- Sessions ---
export async function createSession(data: {
  topic?: string;
  document_id?: string;
  language: string;
  learner_level: string;
  duration_minutes: number;
  goal?: string;
}) {
  return apiFetch("/sessions", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function startSession(sessionId: string) {
  return apiFetch(`/sessions/${sessionId}/start`, { method: "POST" });
}

export async function submitAnswer(sessionId: string, data: {
  question_id: string;
  answer: string;
  concept?: string;
}) {
  return apiFetch(`/sessions/${sessionId}/answer`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getSessionProgress(sessionId: string) {
  return apiFetch(`/sessions/${sessionId}/progress`);
}

export async function getSessionReport(sessionId: string) {
  return apiFetch(`/sessions/${sessionId}/report`);
}

// --- Assessment ---
export async function generateQuiz(sessionId: string) {
  return apiFetch(`/assessment/${sessionId}/quiz`, { method: "POST" });
}

export async function submitQuiz(sessionId: string, answers: unknown[]) {
  return apiFetch(`/assessment/${sessionId}/submit`, {
    method: "POST",
    body: JSON.stringify(answers),
  });
}

// --- Video ---
export async function generateVideo(data: {
  session_id: string;
  segment_id: string;
  script: string;
  visual_type: string;
  language: string;
}) {
  return apiFetch("/video/generate", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getVideoStatus(segmentId: string) {
  return apiFetch(`/video/status/${segmentId}`);
}

// --- Progress ---
export async function getOverallProgress() {
  return apiFetch("/progress");
}

export async function getHistory() {
  return apiFetch("/progress/history");
}
