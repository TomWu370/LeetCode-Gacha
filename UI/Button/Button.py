from abc import ABC, abstractmethod


class Button(ABC):
    buttons = []

    @abstractmethod
    def __init__(self):
        Button.buttons.append(self)

    @abstractmethod
    def process(self):
        pass

    @classmethod
    def init(cls):
        cls.buttons = []

    @classmethod
    def getList(cls):
        return cls.buttons