# 1. Project Title & Tagline

**Adaptive AI Tutor**
*Your Personalized, Intelligent Teaching Companion*

## 2. Problem Statement

One-size-fits-all education leaves many students behind. Learners struggle when materials do not match their language, proficiency level, or learning style. This leads to persistent misconceptions, disengagement, and knowledge gaps that traditional rigid learning platforms fail to address.

## 3. Our Solution

An intelligent, adaptive AI Teacher that builds personalized lesson plans from any topic or uploaded document. It teaches interactively using avatars, voice, and subject-aware visuals, continually evaluating the student's understanding and dynamically adapting its explanations to ensure true mastery of the material.

## 4. Key Features

- **Dynamic Lesson Generation:** Tailored to learner level, language preference, goal, and time constraints.
- **Multimodal Teaching:** Avatar, voice, and subject-aware visual explanations.
- **Interactive Evaluation:** Asks targeted questions and analyzes answers to detect misconceptions.
- **Adaptive Reteaching:** Adjusts explanations dynamically when the student struggles, using alternative analogies.
- **Progress Tracking:** Stores learning progress and recommends next topics or necessary revisions.

## 5. Core User Journey

Upload PDF / Enter Topic ➔ Set Parameters (Level, Language, Time) ➔ AI Generates Lesson ➔ AI Teacher Explains (Avatar + Voice + Visual) ➔ Teacher Asks Question ➔ Student Answers ➔ AI Evaluates (Detects Misconceptions) ➔ AI Re-explains (if needed) ➔ Final Assessment ➔ Learning Report.

## 6. System Architecture

A modular Client-Server architecture integrating a modern Web Frontend, a Python-based Backend API, and specialized AI/ML microservices (RAG, Teacher Agent, Adaptive Learning, Personalization, Avatar/Voice generation).

## 7. Project Directory Structure

```text
ai-teacher/
├── apps/
│   └── web/                              # Team 5
│       ├── app/
│       │   ├── page.tsx
│       │   ├── learn/
│       │   ├── lesson/
│       │   ├── assessment/
│       │   └── progress/
│       ├── components/
│       ├── hooks/
│       └── lib/
│
├── backend/                              # Team 6
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   │       ├── rag/                      # Team 1
│   │       ├── teacher/                  # Team 2
│   │       ├── assessment/               # Team 3
│   │       ├── video/                    # Team 4
│   │       └── learner/                  # Team 6
│   └── tests/
│
├── packages/
│   ├── prompts/                           # Shared prompts
│   ├── types/                             # Shared contracts
│   └── ui/
│
├── data/
│   ├── uploads/
│   └── processed/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   └── demo/
│
├── scripts/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── package.json
└── README.md
```

## 8. Team Responsibilities

| Team | Owner | Primary Deliverable |
| --- | --- | --- |
| 1 | RAG Engineer | Grounded knowledge engine |
| 2 | Teacher Agent Engineer | Lesson planning + teaching brain |
| 3 | Adaptive Learning Engineer | Questions + evaluation + adaptation |
| 4 | Video/Voice Engineer | Avatar + voice + visuals + video |
| 5 | Frontend Engineer | Complete student-facing UI |
| 6 | Backend/Integration Engineer | APIs + DB + integration + deployment |

## 9. Technology Stack

- **Frontend:** Next.js (React), Tailwind CSS
- **Backend:** FastAPI (Python)
- **AI/ML:** LangChain, OpenAI / Llama models
- **Database:** PostgreSQL, Vector DB (e.g., Pinecone/Milvus/Weaviate)
- **Deployment:** Docker, Docker Compose

## 10. AI/ML Architecture

A modular pipeline orchestrating LLMs for reasoning (Teacher Agent), Retrieval-Augmented Generation for factuality (RAG), and generative models for multimodal output (Video/Audio/Images) interacting via well-defined JSON contracts.

## 11. RAG Pipeline

Ingests PDFs, slides, and text documents. Chunks, embeds, and indexes them into a Vector DB. Retrieves highly relevant context to ground the Teacher Agent's lesson planning and explanations, preventing hallucinations.

## 12. AI Teacher Agent

The core orchestration brain. Processes the topic, determines the pedagogical lesson flow, and coordinates with other modules to deliver a structured, engaging lesson.

## 13. Personalization Engine

Tailors the curriculum, pacing, and tone based on the user's proficiency (beginner, intermediate, advanced), language preference, and specific learning goals.

## 14. Adaptive Learning Engine

Monitors student responses, evaluates correctness, identifies specific misconceptions, and prompts the Teacher Agent to adjust the lesson plan and reteach using alternative strategies or analogies.

## 15. Video/Avatar/Voice Pipeline

Generates synchronized audio (Text-to-Speech) and avatar animations to create an engaging, human-like teaching presence.

## 16. Subject-Aware Visual Engine

Produces diagrams, charts, or contextual images to complement the verbal explanation for a given concept, enhancing multimodal learning.

## 17. Multilingual Architecture

End-to-end support for multiple languages (e.g., Hindi, English) encompassing prompt translation, multilingual RAG embedding, and localized TTS.

## 18. Database & Learning Memory

Stores student profiles, interaction history, quiz scores, and persistent knowledge graphs to enable long-term learning tracking and revision recommendations.

## 19. API Documentation

RESTful endpoints defined via OpenAPI/Swagger provided out-of-the-box by FastAPI.
Key shared contracts include `LessonPlan`, `StudentEvaluation`, and `VideoResult`.

## 20. Data Flow

`User Input` ➔ `API Gateway` ➔ `Teacher Agent` ⟷ `RAG & Personalization`
`Teacher Agent` ➔ `Multimodal Engines` ➔ `Frontend Delivery`
`Student Input` ➔ `Adaptive Engine` ➔ `Teacher Agent` ➔ `Adjusted Delivery`

## 21. Installation & Setup

1. Clone the repository
2. Set up a Python virtual environment for the backend
3. Install backend dependencies: `pip install -r requirements.txt`
4. Install frontend dependencies: `cd apps/web && npm install`

## 22. Environment Variables

Copy `.env.example` to `.env`. Required keys include Database URLs, LLM API keys (OpenAI/Anthropic), and Avatar/Voice generation API keys. Never commit `.env` or secrets.

## 23. Running Locally

Run the entire stack via Docker:

```bash
docker-compose up --build
```

Alternatively, run modules separately:

- Backend: `uvicorn app.main:app --reload`
- Frontend: `npm run dev`

## 24. Deployment

Containerized via Docker. Designed to be deployable to AWS/GCP/Azure using managed container services (ECS/Cloud Run) with a managed PostgreSQL and Vector DB.

## 25. Testing

- **Backend:** `pytest` (ensure error handling and API contract adherence)
- **Frontend:** `jest` / React Testing Library
- **CI/CD:** Automated pipelines for linting, testing, and deployment.

## 26. Demo Flow

1. Upload PDF / Enter Topic
2. Set Beginner + Hindi + 20 min
3. AI creates lesson
4. AI Teacher explains with avatar + voice + visual
5. Teacher asks question
6. Student gives WRONG answer
7. AI detects misconception
8. AI re-explains differently
9. Student answers correctly
10. Final quiz
11. Learning report & Next-topic recommendation

## 27. Evaluation Criteria Mapping

- **Personalization:** Customizes to Level, language, and time constraints.
- **Pedagogy:** Adaptive learning, reteaching, misconception detection.
- **Multimodal:** Integrates avatar, voice, and generated visuals.
- **Robustness:** Error handling, grounded RAG to prevent hallucinations.

## 28. Third-Party APIs & Models

- **Text/Reasoning:** OpenAI GPT-4o / Claude 3.5 Sonnet / Gemini 3.7 Flash
- **Voice:** ElevenLabs or similar high-fidelity TTS
- **Avatar:** HeyGen / D-ID API
- **Embeddings:** OpenAI `text-embedding-3-small` or HuggingFace

## 29. Security & Privacy

- Never commit API keys, private uploads or secrets.
- Private uploads are sandboxed per user session.
- Git Branches: `feature/<team>-<task>`, small focused commits.
- PR must include testing steps and schema changes. Do not modify another team's module without coordination.

## 30. Known Limitations

- Video generation latency may introduce delays in real-time interactive teaching.
- RAG accuracy is dependent on the quality and formatting of uploaded documents.
- Avatar/Voice API rate limits and costs may apply at scale.

## 31. Team Members

1. RAG Engineer
2. Teacher Agent Engineer
3. Adaptive Learning Engineer
4. Video/Voice Engineer
5. Frontend Engineer
6. Backend/Integration Engineer
