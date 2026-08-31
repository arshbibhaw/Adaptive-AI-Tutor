# Team 2 — AI Teacher / Lesson Agent Engineer

## Mission
Build the brain that behaves like a teacher instead of a question-answer chatbot.

## Core Loop

```text
Understand → Plan → Explain → Demonstrate
       → Question → Evaluate → Adapt → Continue
```

## Tasklist

### P0 — Learner Understanding
- [ ] Read level.
- [ ] Read existing knowledge.
- [ ] Read goal.
- [ ] Read preferred language.
- [ ] Read teaching style.
- [ ] Read available time.
- [ ] Read desired depth.

### P0 — Lesson Planning
- [ ] Convert topic/material into concepts.
- [ ] Identify prerequisites.
- [ ] Order concepts logically.
- [ ] Allocate time to concepts.
- [ ] Decide checkpoints.
- [ ] Decide examples.
- [ ] Decide visual type.
- [ ] Produce structured `LessonPlan`.

### P0 — Teaching Agent
Implement states:
- [ ] Introduction
- [ ] Explanation
- [ ] Demonstration
- [ ] Question
- [ ] Evaluation
- [ ] Adaptation
- [ ] Continue
- [ ] Final assessment

### P0 — Personalization
Beginner:
- [ ] Simple language.
- [ ] Analogies.
- [ ] Fundamentals.

Intermediate:
- [ ] Technical terms.
- [ ] Practical examples.

Advanced:
- [ ] Technical depth.
- [ ] Mathematics/implementation where appropriate.

### P0 — Time Adaptation
- [ ] 5-minute mode.
- [ ] 20-minute mode.
- [ ] 60-minute mode.
- [ ] Multi-day plan mode.

### P0 — Language
- [ ] Generate lesson in selected language.
- [ ] Preserve context when language changes.
- [ ] Support Hinglish if requested.

### P0 — RAG Integration
- [ ] Retrieve relevant content for each concept.
- [ ] Ground explanations when document mode is active.
- [ ] Keep source metadata.

### P1
- [ ] Teacher personality.
- [ ] Follow-up conversation.
- [ ] Exam mode.
- [ ] Revision mode.

## Agent State

```json
{
  "current_concept": "resistance",
  "completed_concepts": ["voltage", "current"],
  "time_remaining": 11,
  "weak_concepts": [],
  "last_evaluation": null
}
```

## Decision Rules
- Correct → continue or increase difficulty.
- Incorrect → re-explain.
- Repeated incorrect → simplify and retry.
- Time low → prioritize high-value concepts.
- Language changed → preserve state.

## Deliverables
1. Lesson planner.
2. Teacher state machine/graph.
3. Prompt set.
4. LessonPlan schema.
5. RAG integration.
6. Unit tests.
7. Example lesson outputs.

## Handoff
Team 3 sends evaluation results back to this agent. Team 4 consumes lesson segments/scripts. Team 6 exposes the agent through APIs.
