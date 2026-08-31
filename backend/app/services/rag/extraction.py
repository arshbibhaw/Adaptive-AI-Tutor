"""
RAG extraction service.

Extracts text from PDF, DOCX, PPTX, and plain text files.
Preserves page/slide numbers for source metadata.
"""

import logging

logger = logging.getLogger(__name__)


def extract_text(file_path: str, file_type: str) -> list[dict]:
    """
    Extract text from a document file.

    Returns a list of dicts, each representing a page/slide:
    [{"page": 1, "text": "..."}, ...]
    """
    file_type = file_type.lower()

    if file_type == "pdf":
        return _extract_pdf(file_path)
    elif file_type == "docx":
        return _extract_docx(file_path)
    elif file_type == "pptx":
        return _extract_pptx(file_path)
    elif file_type in ("txt", "md"):
        return _extract_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def _extract_pdf(file_path: str) -> list[dict]:
    """Extract text from PDF using PyPDF2."""
    from PyPDF2 import PdfReader

    pages = []
    try:
        reader = PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"page": i + 1, "text": text})
    except Exception as e:
        logger.error("PDF extraction failed for %s: %s", file_path, e)
        raise RuntimeError(f"Failed to extract PDF: {e}") from e

    return pages


def _extract_docx(file_path: str) -> list[dict]:
    """Extract paragraphs and headings from DOCX."""
    from docx import Document

    pages = []
    try:
        doc = Document(file_path)
        current_page = {"page": 1, "text": ""}
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            # Treat headings as section boundaries
            if para.style.name.startswith("Heading"):
                if current_page["text"].strip():
                    pages.append(current_page)
                current_page = {"page": len(pages) + 1, "text": f"## {text}\n"}
            else:
                current_page["text"] += text + "\n"

        if current_page["text"].strip():
            pages.append(current_page)
    except Exception as e:
        logger.error("DOCX extraction failed for %s: %s", file_path, e)
        raise RuntimeError(f"Failed to extract DOCX: {e}") from e

    return pages


def _extract_pptx(file_path: str) -> list[dict]:
    """Extract slide text from PPTX."""
    from pptx import Presentation

    pages = []
    try:
        prs = Presentation(file_path)
        for i, slide in enumerate(prs.slides):
            texts = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    texts.append(shape.text.strip())
            if texts:
                pages.append({"page": i + 1, "text": "\n".join(texts)})
    except Exception as e:
        logger.error("PPTX extraction failed for %s: %s", file_path, e)
        raise RuntimeError(f"Failed to extract PPTX: {e}") from e

    return pages


def _extract_text(file_path: str) -> list[dict]:
    """Extract text from plain text or markdown files."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return [{"page": 1, "text": content}]
    except Exception as e:
        logger.error("Text extraction failed for %s: %s", file_path, e)
        raise RuntimeError(f"Failed to extract text: {e}") from e
