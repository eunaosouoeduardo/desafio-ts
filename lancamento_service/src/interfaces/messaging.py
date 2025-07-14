from abc import ABC, abstractmethod

class IMessagePublisher(ABC):
    @abstractmethod
    def publish(self, routing_key: str, message: dict) -> bool:
        pass