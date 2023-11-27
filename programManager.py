# this class will store and manage runtime variables
from states import States

class Manager:
    def __init__(self, current_aspect=(1600,900), current_degree=0, current_velocity=0, current_state=States.MAIN):
        self.current_aspect = current_aspect
        self.current_degree = current_degree
        self.current_velocity = current_velocity
        self.current_state = current_state

    def setAspect(self, newAspect):
        self.current_aspect = newAspect

    def getAspect(self):
        return self.current_aspect

    def updateSpinner(self, spinner):
        self.current_degree = spinner.getDegree()
        self.current_velocity = spinner.getVelocity()

    def getDegree(self):
        return self.current_degree

    def getVelocity(self):
        return self.current_velocity

    def setState(self, newState):
        self.current_state = newState

    def getState(self):
        return self.current_state