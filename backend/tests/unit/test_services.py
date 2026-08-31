"""
Unit tests for the RAG extraction service.
"""

import os
import tempfile
import pytest

from backend.app.services.rag.extraction import extract_text


class TestTextExtraction:
    """Tests for text file extraction."""

    def test_extract_txt(self):
        """Test extraction from a plain text file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Hello world. This is a test document.")
            f.flush()
            path = f.name

        try:
            result = extract_text(path, "txt")
            assert len(result) == 1
            assert result[0]["page"] == 1
            assert "Hello world" in result[0]["text"]
        finally:
            os.unlink(path)

    def test_extract_unsupported_type(self):
        """Test that unsupported file types raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            extract_text("dummy.xyz", "xyz")


class TestCleaning:
    """Tests for the cleaning service."""

    def test_clean_and_structure(self):
        from backend.app.services.rag.cleaning import clean_and_structure

        pages = [
            {"page": 1, "text": "## Introduction\nThis is the introduction."},
            {"page": 2, "text": "## Chapter 1\nContent of chapter 1."},
        ]
        result = clean_and_structure(pages)

        assert "title" in result
        assert "sections" in result
        assert len(result["sections"]) > 0

    def test_empty_input(self):
        from backend.app.services.rag.cleaning import clean_and_structure

        result = clean_and_structure([])
        assert result["title"] == "Untitled Document"


class TestChunking:
    """Tests for the chunking service."""

    def test_chunk_short_document(self):
        from backend.app.services.rag.chunking import chunk_document

        structured = {
            "title": "Test",
            "sections": [
                {"heading": "Intro", "page": 1, "content": "Short content.", "type": "content"}
            ],
        }
        chunks = chunk_document("doc-1", structured)
        assert len(chunks) >= 1
        assert chunks[0]["document_id"] == "doc-1"
        assert "text" in chunks[0]

    def test_chunk_preserves_metadata(self):
        from backend.app.services.rag.chunking import chunk_document

        structured = {
            "title": "Test",
            "sections": [
                {"heading": "Chapter 1", "page": 3, "content": "Some content.", "type": "chapter"}
            ],
        }
        chunks = chunk_document("doc-2", structured)
        assert chunks[0]["page"] == 3
        assert chunks[0]["chapter"] == "Chapter 1"


class TestAdaptation:
    """Tests for the adaptation engine."""

    def test_correct_increases_difficulty(self):
        from backend.app.services.assessment.adaptation import AdaptationEngine

        engine = AdaptationEngine()
        engine.record_result("voltage", True)
        engine.record_result("voltage", True)
        action = engine.decide_action("voltage")
        assert action["action"] == "increase_difficulty"

    def test_incorrect_re_explains(self):
        from backend.app.services.assessment.adaptation import AdaptationEngine

        engine = AdaptationEngine()
        engine.record_result("resistance", False)
        action = engine.decide_action("resistance")
        assert action["action"] == "re_explain"

    def test_two_incorrect_simplifies(self):
        from backend.app.services.assessment.adaptation import AdaptationEngine

        engine = AdaptationEngine()
        engine.record_result("resistance", False)
        engine.record_result("resistance", False)
        action = engine.decide_action("resistance")
        assert action["action"] == "simplify"

    def test_three_failures_marks_weak(self):
        from backend.app.services.assessment.adaptation import AdaptationEngine

        engine = AdaptationEngine()
        engine.record_result("resistance", False)
        engine.record_result("resistance", False)
        engine.record_result("resistance", False)
        action = engine.decide_action("resistance")
        assert action["action"] == "mark_weak"


class TestLessonState:
    """Tests for the lesson state tracker."""

    def test_initial_state(self):
        from backend.app.services.teacher.lesson_state import LessonState

        state = LessonState()
        assert state.phase == "introduction"
        assert state.current_segment_index == 0
        assert state.total_questions_asked == 0

    def test_record_correct(self):
        from backend.app.services.teacher.lesson_state import LessonState

        state = LessonState()
        state.record_correct()
        assert state.total_correct == 1
        assert state.total_questions_asked == 1
        assert state.consecutive_incorrect == 0

    def test_record_incorrect(self):
        from backend.app.services.teacher.lesson_state import LessonState

        state = LessonState()
        state.record_incorrect()
        assert state.total_correct == 0
        assert state.total_questions_asked == 1
        assert state.consecutive_incorrect == 1

    def test_serialization_roundtrip(self):
        from backend.app.services.teacher.lesson_state import LessonState

        state = LessonState(current_concept="voltage", phase="explanation")
        data = state.to_dict()
        restored = LessonState.from_dict(data)
        assert restored.current_concept == "voltage"
        assert restored.phase == "explanation"


class TestPersonalization:
    """Tests for the personalization service."""

    def test_beginner_config(self):
        from backend.app.services.teacher.personalization import get_personalization_context

        ctx = get_personalization_context("beginner", "en")
        assert ctx["use_analogies"] is True
        assert ctx["use_technical_terms"] is False

    def test_advanced_config(self):
        from backend.app.services.teacher.personalization import get_personalization_context

        ctx = get_personalization_context("advanced", "en")
        assert ctx["use_analogies"] is False
        assert ctx["use_technical_terms"] is True

    def test_time_config(self):
        from backend.app.services.teacher.personalization import get_time_config

        config_5 = get_time_config(5)
        assert config_5["mode"] == "quick"
        assert config_5["include_assessment"] is False

        config_20 = get_time_config(20)
        assert config_20["mode"] == "standard"
        assert config_20["include_assessment"] is True
