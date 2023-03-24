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
        """ttl: seconds"""
        self.cache = TTLCache(maxsize, ttl)

    def get(self, key):
        data = self.cache.get(key)
        return data

    def set(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache.clear()



if __name__ == "__main__":
    import time
    cache = StaticCache(3, 3)
    cache.set(0, "zeroo")
    time.sleep(4)
    print(cache.get(0))
