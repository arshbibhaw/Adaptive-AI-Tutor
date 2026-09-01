# Team 5 — Frontend / Student Experience Engineer

## Mission

Build the complete student-facing interface for the AI Teacher.

## Tasklist

### P0 — Start Learning

Create:

- [ ] Topic input.
- [ ] File upload.
- [ ] Level selection.
- [ ] Language selection.
- [ ] Goal input.
- [ ] Time selection.
- [ ] Teaching style/depth.

### P0 — Material Screen

- [ ] Show uploaded file.
- [ ] Show document processing status.
- [ ] Display chapter/section outline.
- [ ] Allow chapter selection.

### P0 — Lesson Plan Screen

Display:

- [ ] Lesson title.
- [ ] Concepts.
- [ ] Estimated time.
- [ ] Language.
- [ ] Difficulty.
- [ ] Lesson sequence.

### P0 — Teaching Room

Must show:

- [ ] AI avatar/video.
- [ ] Voice/video controls.
- [ ] Current concept.
- [ ] Visuals.
- [ ] Subtitles.
- [ ] Time/progress.
- [ ] Question.
- [ ] Answer input.
- [ ] Teacher feedback.
- [ ] Visible adaptation state.

### P0 — Assessment

- [ ] Display questions.
- [ ] Accept answers.
- [ ] Submit.
- [ ] Show feedback.
- [ ] Show score.

### P0 — Learning Report

Display:

- [ ] Overall score.
- [ ] Strong concepts.
- [ ] Weak concepts.
- [ ] Misconceptions.
- [ ] Revision recommendation.
- [ ] Next topic.

### P0 — Progress

- [ ] Learning history.
- [ ] Topic progress.
- [ ] Scores.
- [ ] Current learning path.

### P1

- [ ] Dark mode.
- [ ] Accessibility controls.
- [ ] Teacher personality selector.
- [ ] Study planner.
- [ ] Flashcards.

## Critical UX

The judge should understand the product immediately.

The adaptive moment should be obvious:

`Student wrong → Teacher detects issue → Teacher says let's try another way → New explanation/question`

## Expected API Calls

```text
POST /documents/upload
GET  /documents/{id}/outline
POST /sessions
POST /sessions/{id}/start
POST /sessions/{id}/answer
GET  /sessions/{id}/progress
GET  /sessions/{id}/report
```

## UI States

Handle:

- [ ] Loading.
- [ ] Processing.
- [ ] Video generating.
- [ ] Video ready.
- [ ] API failure.
- [ ] Empty state.
- [ ] Invalid upload.

## Deliverables

1. Complete UI.
2. Responsive design.
3. API integration.
4. Demo flow.
5. Error/loading states.
6. Frontend tests where practical.

## Handoff

Use Team 6 API contracts. Do not duplicate backend/AI logic in the frontend.
