# API Contracts

## Base URL

`http://localhost:8000/api`

## Authentication

All endpoints except `/learner/register` and `/learner/login` require a Bearer token.

```
Authorization: Bearer <access_token>
```

---

## Auth Endpoints

### POST /learner/register
Register a new user.

**Request:**
```json
{ "email": "user@example.com", "password": "pass123", "full_name": "John" }
```

**Response:**
```json
{ "access_token": "...", "token_type": "bearer" }
```

### POST /learner/login
Log in.

**Request:**
```json
{ "email": "user@example.com", "password": "pass123" }
```

**Response:**
```json
{ "access_token": "...", "token_type": "bearer" }
```

---

## Learner Profile

### GET /learner/profile
### PUT /learner/profile

**Request:**
```json
{ "level": "beginner", "language": "en", "goals": "exam prep" }
```

---

## Documents

### POST /documents/upload
Upload file as multipart/form-data.

### POST /documents/{id}/index
Index document for RAG retrieval.

### GET /documents/{id}/outline
Get document structural outline.

---

## Sessions

### POST /sessions
Create a new teaching session.

**Request:**
```json
{
  "topic": "Ohm's Law",
  "language": "en",
  "learner_level": "beginner",
  "duration_minutes": 20,
  "goal": "exam prep"
}
```

### POST /sessions/{id}/start
Start the session (generates lesson plan).

### POST /sessions/{id}/answer
Submit a student answer.

**Request:**
```json
{ "question_id": "q1", "answer": "my answer", "concept": "voltage" }
```

### GET /sessions/{id}/progress
### GET /sessions/{id}/report

---

## Assessment

### POST /assessment/{session_id}/quiz
Generate final quiz.

### POST /assessment/{session_id}/submit
Submit quiz answers.

---

## Video

### POST /video/generate

**Request:**
```json
{
  "session_id": "...",
  "segment_id": "s1",
  "script": "...",
  "visual_type": "diagram",
  "language": "en"
}
```

### GET /video/status/{segment_id}

---

## Progress

### GET /progress
Overall learning progress.

### GET /progress/history
Session history.
