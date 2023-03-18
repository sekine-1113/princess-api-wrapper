from cachetools import TTLCache


class StaticCache:
    def __init__(self, maxsize: int, ttl: int) -> None:
        self.cache = TTLCache(maxsize, ttl)

    def get(self, key):
        data = self.cache.get(key)
        return data

    def set(self, key, value):
        self.cache[key] = value
