"""Long-term memory module.

SQLite-based persistent storage for facts and project data.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class LongTermMemory:
    """Persistent SQLite storage for long-term facts."""

    def __init__(self, db_path: Path):
        """Initialize long-term memory with SQLite database.

        Args:
            db_path: Path to the SQLite database file.
        """
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self._db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_db(self) -> None:
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                project_id TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_key ON facts(key)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_project ON facts(project_id)
        """)
        conn.commit()

    def store(self, key: str, value: Any, project_id: str) -> int:
        """Store a fact in long-term memory.

        Args:
            key: Storage key.
            value: Value to store (will be converted to string).
            project_id: Project identifier for isolation.

        Returns:
            The ID of the inserted row.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO facts (key, value, timestamp, project_id) VALUES (?, ?, ?, ?)",
            (key, str(value), timestamp, project_id)
        )
        conn.commit()
        return cursor.lastrowid

    def retrieve(self, key: str, project_id: Optional[str] = None) -> Optional[str]:
        """Retrieve a fact by key.

        Args:
            key: Storage key.
            project_id: Optional project filter.

        Returns:
            Value if found, None otherwise.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        if project_id:
            cursor.execute(
                "SELECT value FROM facts WHERE key = ? AND project_id = ? ORDER BY id DESC LIMIT 1",
                (key, project_id)
            )
        else:
            cursor.execute(
                "SELECT value FROM facts WHERE key = ? ORDER BY id DESC LIMIT 1",
                (key,)
            )

        row = cursor.fetchone()
        return row["value"] if row else None

    def retrieve_all(self, project_id: str) -> list[dict[str, Any]]:
        """Retrieve all facts for a project.

        Args:
            project_id: Project identifier.

        Returns:
            List of fact dictionaries.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, key, value, timestamp, project_id FROM facts WHERE project_id = ? ORDER BY id DESC",
            (project_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def delete(self, key: str, project_id: str) -> bool:
        """Delete a fact by key and project.

        Args:
            key: Storage key.
            project_id: Project identifier.

        Returns:
            True if deleted, False if not found.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM facts WHERE key = ? AND project_id = ?",
            (key, project_id)
        )
        conn.commit()
        return cursor.rowcount > 0

    def clear_project(self, project_id: str) -> int:
        """Clear all facts for a project.

        Args:
            project_id: Project identifier.

        Returns:
            Number of facts deleted.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facts WHERE project_id = ?", (project_id,))
        conn.commit()
        return cursor.rowcount

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
