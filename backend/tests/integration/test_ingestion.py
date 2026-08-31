"""
Integration tests for the RAG ingestion pipeline.
"""

import os
import tempfile
import pytest

from backend.app.services.rag.ingestion import validate_file, save_upload


class TestFileValidation:
    """Tests for file validation."""

    def test_valid_pdf(self):
        error = validate_file("test.pdf", 1000)
        assert error is None

    def test_valid_docx(self):
        error = validate_file("report.docx", 5000)
        assert error is None

    def test_unsupported_type(self):
        error = validate_file("image.jpg", 1000)
        assert error is not None
        assert "Unsupported" in error

    def test_file_too_large(self):
        error = validate_file("huge.pdf", 100 * 1024 * 1024)
        assert error is not None
        assert "too large" in error

    def test_no_extension(self):
        error = validate_file("noextension", 1000)
        assert error is not None


class TestSaveUpload:
    """Tests for file saving."""

    @pytest.mark.asyncio
    async def test_save_upload_creates_file(self):
        content = b"test content"
        doc_id, path = await save_upload(content, "test.txt")

        assert doc_id
        assert os.path.exists(path)

        # Cleanup
        os.unlink(path)
