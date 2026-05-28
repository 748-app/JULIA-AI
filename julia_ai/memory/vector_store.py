"""Vector store module for semantic search and RAG.

Lightweight stub implementation - ChromaDB disabled due to disk space constraints.
This module will be fully implemented in Phase 4 when storage is available.
"""

from pathlib import Path
from typing import Any, Optional


class VectorStore:
    """Stub vector store - returns empty results but maintains API compatibility."""

    def __init__(self, persist_directory: Path):
        """Initialize vector store (stub mode).

        Args:
            persist_directory: Directory for persistent storage (unused in stub).
        """
        self._persist_dir = persist_directory
        self._documents: dict[str, dict[str, Any]] = {}

    def is_available(self) -> bool:
        """Check if vector store is available.

        Returns:
            True (stub is always available).
        """
        return True

    def add(self, id: str, text: str, metadata: Optional[dict[str, Any]] = None) -> bool:
        """Add a document to the vector store (in-memory stub).

        Args:
            id: Unique identifier for the document.
            text: Text content to store.
            metadata: Optional metadata dictionary.

        Returns:
            True if added successfully.
        """
        self._documents[id] = {
            "text": text,
            "metadata": metadata or {}
        }
        return True

    def search(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search for documents (simple keyword match in stub).

        Args:
            query: Search query text.
            n_results: Number of results to return.

        Returns:
            List of matching documents (empty in stub).
        """
        # Return empty list - no semantic search in stub mode
        return []

    def delete(self, id: str) -> bool:
        """Delete a document by ID.

        Args:
            id: Document identifier.

        Returns:
            True if deleted, False otherwise.
        """
        if id in self._documents:
            del self._documents[id]
            return True
        return False

    def count(self) -> int:
        """Get the number of documents in the store.

        Returns:
            Number of stored documents.
        """
        return len(self._documents)

    def clear(self) -> bool:
        """Clear all documents from the store.

        Returns:
            True if cleared.
        """
        self._documents.clear()
        return True
