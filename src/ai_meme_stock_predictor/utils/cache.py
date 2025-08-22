from cachetools import TTLCache
from functools import lru_cache

# Short-lived cache for API responses
api_cache = TTLCache(maxsize=1024, ttl=60)

@lru_cache(maxsize=128)
def static_normalization(term: str) -> str:
    return term.lower().strip()
