from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseLLM(ABC):

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def chat(
        self, messages: List[Dict[str, str]]
        ) -> str:
        raise NotImplementedError
