from abc import ABC, abstractmethod

from cachetools import TTLCache


class Cache(ABC):

    @abstractmethod
    def get(self, key):
        ...

    @abstractmethod
    def set(self, key, value):
        ...


class StaticCache(Cache):
    def __init__(self, maxsize: int, ttl: int) -> None:
        self.cache = TTLCache(maxsize, ttl)

    def get(self, key):
        data = self.cache.get(key)
        return data

    def set(self, key, value):
        self.cache[key] = value
