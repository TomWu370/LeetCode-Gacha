from enum import Enum


class States(Enum):
    # STATES
    MAIN = 0
    RESULT = 1
    SPIN = 2
    INSUFFICIENT = 3
    RESIZE = 4


class State:
    def __init__(self):
        self.__state = States.MAIN

    def setState(self, new_state):
        self.__state = new_state

    def getState(self):
        return self.__state

    def isState(self, other_state):
        return self.__state == other_state
