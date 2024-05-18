from abc import ABC, abstractmethod
from pinecone.config import Config
from typing import Callable, Type, Generic, TypeVar

T = TypeVar("T")

class PineconePlugin(ABC, Generic[T]):
    @abstractmethod
    def __init__(self, client_builder: Callable[[Type[T]], T], config: Config):
        pass
