import pytest

from unittest.mock import MagicMock

from app.services.document_service import DocumentService


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def ai_client():
    return MagicMock()


@pytest.fixture
def service(repository, ai_client):
    return DocumentService(repository=repository, ai_client=ai_client)
