from enum import Enum


class StateType(Enum):
    # STATES
    MAIN = 0
    RESULT = 1
    SPIN = 2
    INSUFFICIENT = 3
    RESIZE = 4


class State:
    def __init__(self, state=StateType.MAIN):
        self.__state = state

    def setState(self, new_state):
        self.__state = new_state

    def getState(self):
        return self.__state

    def isState(self, other_state):
        return self.__state == other_state
