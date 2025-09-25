from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class CachedData:
    key: str
    value: Any
    timestamp: datetime
    ttl_seconds: int

    def is_valid(self) -> bool:
        age = (datetime.now() - self.timestamp).total_seconds()
        return age < self.ttl_seconds

    def age_minutes(self) -> float:
        age = (datetime.now() - self.timestamp).total_seconds()
        return age / 60

class CacheManager:
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self.cache: Dict[str, CachedData] = {}
        self.default_ttl = default_ttl
        self.hit_count = 0
        self.miss_count = 0
        self.invalidation_count = 0

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            self.miss_count += 1
            return None

        cached_data = self.cache[key]

        if not cached_data.is_valid():
            # Data expired, remove it
            del self.cache[key]
            self.miss_count += 1
            return None

        self.hit_count += 1
        return cached_data.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if ttl is None:
            ttl = self.default_ttl

        self.cache[key] = CachedData(
            key=key,
            value=value,
            timestamp=datetime.now(),
            ttl_seconds=ttl
        )

    def invalidate(self, key: str) -> bool:
        if key in self.cache:
            del self.cache[key]
            self.invalidation_count += 1
            return True
        return False

    def invalidate_pattern(self, pattern: str):
        keys_to_delete = [key for key in self.cache.keys() if pattern in key]
        for key in keys_to_delete:
            del self.cache[key]
            self.invalidation_count += 1

    def is_valid(self, key: str) -> bool:
        if key not in self.cache:
            return False
        return self.cache[key].is_valid()

    def get_age(self, key: str) -> Optional[float]:
        if key not in self.cache:
            return None
        return self.cache[key].age_minutes()

    def clear_expired(self):
        expired_keys = [key for key, data in self.cache.items() if not data.is_valid()]
        for key in expired_keys:
            del self.cache[key]

    def clear_all(self):
        self.cache.clear()

    def get_stats(self) -> Dict:
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0

        return {
            "total_cached": len(self.cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": f"{hit_rate:.1f}%",
            "invalidations": self.invalidation_count,
            "cache_size_kb": self._estimate_size() / 1024
        }

    def _estimate_size(self) -> int:
        # Rough estimate of cache size in bytes
        total_size = 0
        for key, cached_data in self.cache.items():
            total_size += len(key)
            total_size += len(str(cached_data.value))
        return total_size

    def get_cached_with_metadata(self, key: str) -> Optional[Dict]:
        if key not in self.cache:
            return None

        cached_data = self.cache[key]
        if not cached_data.is_valid():
            return None

        return {
            "value": cached_data.value,
            "cached_at": cached_data.timestamp.isoformat(),
            "age_minutes": cached_data.age_minutes(),
            "expires_in_seconds": cached_data.ttl_seconds - (datetime.now() - cached_data.timestamp).total_seconds()
        }