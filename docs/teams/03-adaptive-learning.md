# Team 3 — Interactive Assessment & Adaptive Learning Engineer

## Mission

Make the AI Teacher respond intelligently to student performance.

## Tasklist

### P0 — Question Generation

Generate:

- [ ] MCQs.
- [ ] Short answers.
- [ ] Conceptual questions.
- [ ] Numerical/problem-solving questions.
- [ ] Application questions.
- [ ] Explain-in-your-own-words questions.

Questions must match:

- [ ] Concept.
- [ ] Student level.
- [ ] Lesson stage.
- [ ] Language.

### P0 — Answer Evaluation

Evaluate:

- [ ] Correct.
- [ ] Partially correct.
- [ ] Incorrect.
- [ ] Off-topic.
- [ ] Low-confidence/guess.

Return score + explanation + confidence.

### P0 — Misconception Detection

For incorrect answers:

- [ ] Identify likely misconception.
- [ ] Identify affected concept.
- [ ] Select remediation strategy.
- [ ] Avoid merely saying "wrong."

### P0 — Adaptive Response

Possible actions:

- [ ] Continue.
- [ ] Increase difficulty.
- [ ] Keep difficulty.
- [ ] Simplify.
- [ ] Use analogy.
- [ ] Give worked example.
- [ ] Show visual.
- [ ] Re-teach.
- [ ] Re-test.
- [ ] Mark weak concept.

### P0 — Final Assessment

- [ ] Generate final quiz.
- [ ] Evaluate it.
- [ ] Calculate score.
- [ ] Identify strong/weak concepts.
- [ ] Recommend revision.
- [ ] Recommend next topic.

### P0 — Progress

Track:

- [ ] Attempts.
- [ ] Mastery.
- [ ] Weak concepts.
- [ ] Strong concepts.
- [ ] Misconceptions.

### P1

- [ ] Spaced revision recommendations.
- [ ] Personalized homework.
- [ ] Flashcards.
- [ ] Exam mode.

## MVP Adaptation Rule

```text
2 correct → increase difficulty
1 incorrect → re-explain
2 incorrect on same concept → simplify
3 failures → mark weak + recommend revision
```

## Evaluation Contract

```json
{
  "question_id": "q1",
  "correct": false,
  "score": 0.2,
  "concept": "resistance",
  "misconception": "inverse relationship misunderstood",
  "confidence": 0.94,
  "next_action": "analogy_then_retest",
  "difficulty": "easy"
}
```

## Critical Demo

The system MUST demonstrate:

```text
Wrong answer
 ↓
Misconception detected
 ↓
Alternative explanation
 ↓
New question
 ↓
Correct answer
```

## Deliverables

1. Question generator.
2. Evaluator.
3. Misconception detector.
4. Adaptation rules.
5. Final assessment.
6. Learning report generator.
7. Tests.

## Handoff

Team 2 consumes `StudentEvaluation` to decide the next lesson state. Team 6 persists evaluations/progress. Team 5 displays them.
