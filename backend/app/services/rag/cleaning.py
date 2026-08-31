"""
RAG cleaning service.

Cleans extracted text and detects document structure
(chapters, sections, definitions, examples).
"""

import logging
import re

logger = logging.getLogger(__name__)


def clean_and_structure(raw_pages: list[dict]) -> dict:
    """
    Clean raw extracted pages and detect document structure.

    Returns a structured document dict:
    {
        "title": str,
        "sections": [{"heading": str, "page": int, "content": str, "type": str}],
        "full_text": str,
    }
    """
    sections = []
    full_text_parts = []
    title = ""

    for page_data in raw_pages:
        text = _clean_text(page_data["text"])
        page_num = page_data.get("page", 0)

        if not text.strip():
            continue

        full_text_parts.append(text)

        # Detect headings and sections within the text
        page_sections = _detect_sections(text, page_num)

        if not title and page_sections:
            title = page_sections[0].get("heading", "Untitled")

        sections.extend(page_sections)

    if not sections and full_text_parts:
        # No structure detected; treat entire document as one section
        sections.append({
            "heading": "Content",
            "page": 1,
            "content": "\n".join(full_text_parts),
            "type": "content",
        })

    if not title:
        title = "Untitled Document"

    return {
        "title": title,
        "sections": sections,
        "full_text": "\n\n".join(full_text_parts),
    }


def _clean_text(text: str) -> str:
    """Remove headers, footers, excessive whitespace."""
    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove lines that are just page numbers
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    # Normalize whitespace within lines
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _detect_sections(text: str, page: int) -> list[dict]:
    """
    Detect sections within a page of text.

    Looks for heading patterns (numbered sections, markdown headings, uppercase lines).
    """
    sections = []
    lines = text.split("\n")
    current_heading = ""
    current_content = []
    current_type = "content"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            current_content.append("")
            continue

        # Detect markdown-style headings
        if re.match(r"^#{1,4}\s+", stripped):
            if current_heading or current_content:
                sections.append({
                    "heading": current_heading or "Content",
                    "page": page,
                    "content": "\n".join(current_content).strip(),
                    "type": current_type,
                })
            current_heading = re.sub(r"^#+\s*", "", stripped)
            current_content = []
            current_type = "section"

        # Detect numbered chapter/section headings
        elif re.match(r"^(Chapter|Section|Part)\s+\d+", stripped, re.IGNORECASE):
            if current_heading or current_content:
                sections.append({
                    "heading": current_heading or "Content",
                    "page": page,
                    "content": "\n".join(current_content).strip(),
                    "type": current_type,
                })
            current_heading = stripped
            current_content = []
            current_type = "chapter"

        # Detect definition patterns
        elif re.match(r"^(Definition|Theorem|Lemma|Corollary|Axiom)\s*[\d.:]*", stripped, re.IGNORECASE):
            current_content.append(stripped)
            current_type = "definition"

        # Detect example patterns
        elif re.match(r"^(Example|Exercise|Problem)\s*[\d.:]*", stripped, re.IGNORECASE):
            current_content.append(stripped)
            current_type = "example"

        else:
            current_content.append(stripped)

    # Flush remaining content
    if current_heading or current_content:
        sections.append({
            "heading": current_heading or "Content",
            "page": page,
            "content": "\n".join(current_content).strip(),
            "type": current_type,
        })

    return sections
