from __future__ import annotations

import time
from typing import Any, Callable, Dict, Optional, Tuple


class TTLCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, Tuple[float, Any]] = {}

    def _expired(self, timestamp: float) -> bool:
        return (time.time() - timestamp) > self.ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        timestamp, value = item
        if self._expired(timestamp):
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (time.time(), value)

    def get_or_set(self, key: str, func: Callable[[], Any]) -> Any:
        cached = self.get(key)
        if cached is not None:
            return cached
        value = func()
        self.set(key, value)
        return value


cache = TTLCache(ttl_seconds=3600)  # 1 hour cache — conserves API quota
