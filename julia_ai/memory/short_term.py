"""Short-term memory module.

Simple in-memory dictionary with TTL (time-to-live) support.
Used for session-based temporary storage.
"""

import time
from typing import Any, Optional


class ShortTermMemory:
    """In-memory storage with automatic expiration."""

    def __init__(self, ttl_seconds: int = 300):
        """Initialize short-term memory.

        Args:
            ttl_seconds: Time-to-live for stored items (default: 300s).
        """
        self._store: dict[str, tuple[Any, float]] = {}
        self._ttl = ttl_seconds

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store a value with optional custom TTL.

        Args:
            key: Storage key.
            value: Value to store.
            ttl: Optional custom TTL in seconds.
        """
        expire_time = time.time() + (ttl if ttl is not None else self._ttl)
        self._store[key] = (value, expire_time)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value if not expired.

        Args:
            key: Storage key.

        Returns:
            Value if found and not expired, None otherwise.
        """
        if key not in self._store:
            return None

        value, expire_time = self._store[key]
        if time.time() > expire_time:
            del self._store[key]
            return None

        return value

    def delete(self, key: str) -> bool:
        """Delete a key from storage.

        Args:
            key: Storage key.

        Returns:
            True if deleted, False if key didn't exist.
        """
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all stored values."""
        self._store.clear()

    def cleanup_expired(self) -> int:
        """Remove all expired entries.

        Returns:
            Number of entries removed.
        """
        now = time.time()
        expired_keys = [
            k for k, (_, expire_time) in self._store.items()
            if now > expire_time
        ]
        for key in expired_keys:
            del self._store[key]
        return len(expired_keys)

    def is_expired(self, key: str) -> bool:
        """Check if a key is expired without retrieving it.

        Args:
            key: Storage key.

        Returns:
            True if expired or not found, False otherwise.
        """
        if key not in self._store:
            return True
        _, expire_time = self._store[key]
        return time.time() > expire_time
