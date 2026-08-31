# Team 4 — AI Teacher Video, Voice & Visual Engineer

## Mission
Turn lesson segments into a convincing teaching video using an avatar, natural voice and useful visuals.

## Tasklist

### P0 — Voice
- [ ] Integrate TTS.
- [ ] Select natural voice.
- [ ] Support target languages.
- [ ] Control speaking speed where possible.
- [ ] Generate subtitles/transcript.

### P0 — Avatar
- [ ] Integrate AI avatar provider.
- [ ] Select teacher avatar.
- [ ] Pass lesson script.
- [ ] Generate talking-head teaching output.
- [ ] Handle generation status/failure.

### P0 — Visuals
Implement subject-aware visual selection:

- [ ] Math → equations/graphs/steps.
- [ ] Physics → diagrams/formulas/process.
- [ ] Biology → labeled diagrams.
- [ ] History → timelines/maps.
- [ ] Programming → code/output/flow.
- [ ] AI/ML → architecture/graphs.

### P0 — Synchronization
- [ ] Match visual duration to speech.
- [ ] Show important text/equations while spoken.
- [ ] Include subtitles.
- [ ] Keep visuals readable.

### P0 — Video Pipeline

```text
Lesson Segment
 ↓
Script
 ↓
Visual Plan
 ↓
TTS
 ↓
Avatar
 ↓
Visual composition
 ↓
Final video
```

### P1
- [ ] Dynamic animations.
- [ ] Interactive diagrams.
- [ ] Multiple teacher personalities.
- [ ] Real-time voice conversation.

### P2
- [ ] Emotion-aware avatar.
- [ ] Advanced subject simulations.

## Video Contract

```json
{
  "segment_id": "s1",
  "status": "completed",
  "video_url": "...",
  "duration_seconds": 35,
  "language": "hi"
}
```

## Critical Requirement
Do NOT make only:

`Generated text → talking avatar`

The output must visibly contain meaningful educational visuals.

## Deliverables
1. TTS integration.
2. Avatar integration.
3. Visual generation/selection.
4. Video composition pipeline.
5. Subtitle support.
6. Video API.
7. Failure handling.
8. Demo video segment.

## Handoff
Team 2 provides lesson segments. Team 6 integrates the video service. Team 5 embeds the final video/status in the UI.
