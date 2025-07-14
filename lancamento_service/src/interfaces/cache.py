from abc import ABC, abstractmethod

class ICacheHandler(ABC):
    def get(self, key: str) -> any:
        pass

    @abstractmethod
    def set(self, key: str, value: any, ttl: int = None) -> bool:
        pass

    @abstractmethod
    def invalidate(self, key: str) -> bool:
        pass

    