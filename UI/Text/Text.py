from abc import ABC, abstractmethod


class Text(ABC):
    texts = []

    @abstractmethod
    def __init__(self):
        Text.texts.append(self)

    @abstractmethod
    def process(self):
        pass

    @classmethod
    def init(cls):
        cls.texts = []

    @classmethod
    def getList(cls):
        return cls.texts
