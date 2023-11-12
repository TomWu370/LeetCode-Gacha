from enum import Enum


class States(Enum):
    # STATES
    MAIN = 0
    RESULT = 1
    SPIN = 2

class State():
    def __init__(self):
        self.state = States.MAIN

    def setState(self, new_state):
        self.state = new_state

    def getState(self):
        return self.state

    def isState(self, other_state):
        return self.state == other_state