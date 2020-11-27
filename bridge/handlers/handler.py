from abc import ABC, abstractmethod

class Handler(ABC):
    pass

    @abstractmethod
    def handle(self, message):
        pass

    @abstractmethod
    def get_latest(self):
        pass