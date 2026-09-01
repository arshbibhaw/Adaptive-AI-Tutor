# Team 6 — Backend, Database, Integration & Deployment Engineer

## Mission
Make every module work as one reliable application and deploy it.

## Tasklist

### P0 — Backend
- [ ] Create FastAPI application.
- [ ] Configure CORS.
- [ ] Centralize configuration.
- [ ] Add request validation.
- [ ] Add error handling.
- [ ] Add logging.

### P0 — Database
Create models/tables for:
- [x] Users.
- [x] Learner profiles.
- [x] Documents.
- [x] Sessions.
- [x] Lesson plans.
- [x] Interactions.
- [x] Assessments.
- [x] Progress.
- [x] Learning reports.

### P0 — Learner Profile
Store:
- [x] Level.
- [x] Language.
- [x] Goals.
- [x] Preferences.
- [x] Strong concepts.
- [x] Weak concepts.
- [x] Learning history.

### P0 — API Layer
Implement/coordinate:
- [ ] Document upload.
- [ ] Document outline.
- [ ] Session creation.
- [ ] Lesson generation.
- [ ] Answer submission.
- [ ] Evaluation.
- [ ] Video status.
- [ ] Final assessment.
- [ ] Progress/report.

### P0 — Integration
Connect:

```text
Frontend
   ↓
FastAPI
   ├── RAG
   ├── Teacher Agent
   ├── Assessment
   ├── Video
   └── Learner DB
```

### P0 — File Storage
- [ ] Store uploaded files safely.
- [ ] Do not expose private files publicly by default.
- [ ] Track processing status.
- [ ] Handle cleanup.

### P0 — Authentication
- [ ] User registration/login or chosen auth provider.
- [ ] Protect user-specific data.
- [ ] Ensure one user cannot access another user's documents/progress.

### P0 — Deployment
- [ ] Deploy backend.
- [ ] Configure database.
- [ ] Configure vector DB.
- [ ] Configure storage.
- [ ] Configure environment variables.
- [ ] Deploy frontend connection.
- [ ] Test production flow.

### P1
- [ ] Background job queue.
- [ ] Redis/cache.
- [ ] Rate limiting.
- [ ] Analytics.
- [ ] Monitoring.

## Database Relationship

```text
User
 ├── LearnerProfile
 ├── Documents
 └── Sessions
       ├── LessonPlan
       ├── Interactions
       ├── Assessments
       └── LearningReport

Progress belongs to User + Concept
```

## Environment

```text
LLM_API_KEY=
EMBEDDING_API_KEY=
VECTOR_DB_URL=
VECTOR_DB_KEY=
DATABASE_URL=
TTS_API_KEY=
AVATAR_API_KEY=
AUTH_SECRET=
STORAGE_URL=
```

Never commit real values.

## Integration Test

Run the full journey:

```text
Upload PDF
 ↓
Index document
 ↓
Create learner profile
 ↓
Generate lesson
 ↓
Generate video
 ↓
Play video
 ↓
Answer question
 ↓
Evaluate
 ↓
Adapt
 ↓
Final assessment
 ↓
Save report
 ↓
Reload page
 ↓
Progress still exists
```

## Deliverables
1. Backend repository/module.
2. Database schema/migrations.
3. API documentation.
4. Integration tests.
5. Deployment.
6. `.env.example`.
7. Production setup guide.
8. Final end-to-end demo environment.

## Final Responsibility
Before submission, Team 6 coordinates with all teams and confirms that the complete system works from **student input to learning report**.
