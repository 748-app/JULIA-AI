"""Vector store module for semantic search and RAG.

Uses ChromaDB for local vector storage and similarity search.
Prepares the system for future RAG (Retrieval-Augmented Generation).
"""

from pathlib import Path
from typing import Any, Optional

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


class VectorStore:
    """ChromaDB-based vector storage for semantic search."""

    def __init__(self, persist_directory: Path):
        """Initialize vector store with ChromaDB.

        Args:
            persist_directory: Directory for persistent storage.
        """
        self._persist_dir = persist_directory
        self._client: Optional[Any] = None
        self._collection: Optional[Any] = None

        if not CHROMA_AVAILABLE:
            return

        # Initialize ChromaDB in persistent mode
        self._client = chromadb.PersistentClient(
            path=str(persist_directory)
        )
        self._collection = self._client.get_or_create_collection(
            name="julia_memory",
            metadata={"description": "JULIA AI memory collection"}
        )

    def is_available(self) -> bool:
        """Check if ChromaDB is available.

        Returns:
            True if ChromaDB is installed and initialized.
        """
        return CHROMA_AVAILABLE and self._client is not None

    def add(self, id: str, text: str, metadata: Optional[dict[str, Any]] = None) -> bool:
        """Add a document to the vector store.

        Args:
            id: Unique identifier for the document.
            text: Text content to embed and store.
            metadata: Optional metadata dictionary.

        Returns:
            True if added successfully, False otherwise.
        """
        if not self.is_available():
            return False

        try:
            self._collection.upsert(
                ids=[id],
                documents=[text],
                metadatas=[metadata or {}]
            )
            return True
        except Exception:
            return False

    def search(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search for similar documents.

        Args:
            query: Search query text.
            n_results: Number of results to return.

        Returns:
            List of matching documents with metadata.
        """
        if not self.is_available():
            return []

        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=n_results
            )
            # Format results
            if results["ids"] and results["ids"][0]:
                matches = []
                for i, doc_id in enumerate(results["ids"][0]):
                    match = {
                        "id": doc_id,
                        "text": results["documents"][0][i] if results["documents"] else "",
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    }
                    matches.append(match)
                return matches
            return []
        except Exception:
            return []

    def delete(self, id: str) -> bool:
        """Delete a document by ID.

        Args:
            id: Document identifier.

        Returns:
            True if deleted, False otherwise.
        """
        if not self.is_available():
            return False

        try:
            self._collection.delete(ids=[id])
            return True
        except Exception:
            return False

    def count(self) -> int:
        """Get the number of documents in the store.

        Returns:
            Number of stored documents.
        """
        if not self.is_available():
            return 0

        try:
            return self._collection.count()
        except Exception:
            return 0

    def clear(self) -> bool:
        """Clear all documents from the store.

        Returns:
            True if cleared, False otherwise.
        """
        if not self.is_available():
            return False

        try:
            self._client.delete_collection("julia_memory")
            self._collection = self._client.get_or_create_collection(
                name="julia_memory",
                metadata={"description": "JULIA AI memory collection"}
            )
            return True
        except Exception:
            return False
