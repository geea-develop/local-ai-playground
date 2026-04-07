"""
Cache Plugin
Provides caching functionality for expensive operations
"""

from typing import Any, Callable, Optional


class CachePlugin:
    """Simple in-memory cache plugin"""
    
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache"""
        return self.cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Store value in cache"""
        if len(self.cache) >= self.max_size:
            # Simple eviction: remove oldest key
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value
    
    def has(self, key: str) -> bool:
        """Check if key exists in cache"""
        return key in self.cache
    
    def clear(self) -> None:
        """Clear all cached items"""
        self.cache.clear()
    
    def cached_call(self, func: Callable, key: str, *args, **kwargs) -> Any:
        """Execute function and cache result"""
        if self.has(key):
            return self.get(key)
        result = func(*args, **kwargs)
        self.set(key, result)
        return result


if __name__ == "__main__":
    cache = CachePlugin(max_size=10)
    
    def expensive_operation(x: int) -> int:
        return x * x
    
    # First call - computes result
    result1 = cache.cached_call(expensive_operation, "square_5", 5)
    print(f"First call: {result1}")
    
    # Second call - retrieves from cache
    result2 = cache.cached_call(expensive_operation, "square_5", 5)
    print(f"Second call (cached): {result2}")
    
    print(f"Cache contents: {cache.cache}")
