# Team 1 — RAG & Educational Material Engineer

## Mission
Build the system that understands uploaded educational content and supplies reliable context to the AI Teacher.

## Priority
**P0 = mandatory | P1 = important | P2 = optional**

## Tasklist

### P0 — Document Input
- [ ] Accept PDF.
- [ ] Accept DOCX.
- [ ] Accept PPTX.
- [ ] Accept TXT/Markdown if useful.
- [ ] Validate file type and size.
- [ ] Assign `document_id`.
- [ ] Store file metadata.

### P0 — Extraction
- [ ] Extract text from PDF.
- [ ] Extract paragraphs/headings from DOCX.
- [ ] Extract slide text from PPTX.
- [ ] Preserve page/slide numbers.
- [ ] Clean headers, footers and unnecessary whitespace.
- [ ] Handle extraction failures.

### P0 — Structure Detection
Detect:
- [ ] Chapters
- [ ] Sections
- [ ] Subsections
- [ ] Definitions
- [ ] Examples
- [ ] Important concepts

Create a document outline.

### P0 — RAG
- [ ] Chunk extracted content.
- [ ] Add metadata to every chunk.
- [ ] Generate embeddings.
- [ ] Store embeddings in vector DB.
- [ ] Implement semantic search.
- [ ] Return top relevant chunks.
- [ ] Return source/page metadata.
- [ ] Prevent unrelated context from being returned.

### P0 — Grounding
- [ ] Teacher Agent receives retrieved context.
- [ ] Retrieved content includes source references.
- [ ] Document mode should prefer source-grounded answers.
- [ ] Do not invent missing document information.

### P1
- [ ] Hybrid keyword + semantic retrieval.
- [ ] Reranking.
- [ ] OCR for scanned PDFs.
- [ ] Automatic chapter summaries.

### P2
- [ ] Image/table extraction.
- [ ] Multimodal document understanding.

## Suggested API

`POST /documents/upload`

`POST /documents/{id}/index`

`GET /documents/{id}/outline`

`POST /retrieval/search`

### Retrieval response
```json
{
  "query": "What is Ohm's Law?",
  "chunks": [
    {
      "text": "...",
      "page": 12,
      "chapter": "Chapter 4",
      "score": 0.92
    }
  ]
}
```

## Test Cases
- [ ] Normal PDF.
- [ ] Large PDF.
- [ ] DOCX.
- [ ] PPTX.
- [ ] Unsupported file.
- [ ] Query with no relevant result.
- [ ] Query targeting a specific chapter.

## Deliverables
1. Working ingestion pipeline.
2. Vector DB collection/index.
3. Retrieval API.
4. Document outline API.
5. Tests.
6. Setup documentation.

## Handoff
Team 2 consumes retrieval through the API. Team 6 integrates storage/API.
