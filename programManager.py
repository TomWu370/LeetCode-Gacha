# this class will store and manage runtime variables
import sys

import pygame

from states import States
import database as db
import leetscore


class Manager:
    def __init__(self, current_aspect=(1600, 900), current_degree=0, current_velocity=0, current_state=States.MAIN):
        self.current_aspect = current_aspect
        self.current_degree = current_degree
        self.current_velocity = current_velocity
        self.current_state = current_state

    @staticmethod
    def startUp():
        # get initial data
        username = leetscore.getUsername()
        data, gold = db.refresh()
        return username, data['easy'], data['medium'], data['hard'], gold

    @staticmethod
    def renderButtons(objects):
        for button in objects:
            button.process()

    @staticmethod
    def renderTexts(objects):
        for text in objects:
            text.process()

    @staticmethod
    def displayresult(result, font, screen, colour=(0, 0, 0)):
        textsurface = font.render(result, True, colour)
        textrect = textsurface.get_rect()
        textrect.center = screen.get_rect().center
        screen.blit(textsurface, textrect)

    def processEvents(self, screen, state, spinner):
        for event in pygame.event.get():
            self.exitCheck(event)
            if event.type == pygame.VIDEORESIZE:
                self.setState(state.getState())
                self.setAspect((event.w, event.h))
                self.updateSpinner(spinner)
                state.setState(States.RESIZE)

            # detect maximise/minimise
            elif event.type == pygame.ACTIVEEVENT and event.state == 6:
                self.setState(state.getState())
                self.setAspect(screen.get_size())
                self.updateSpinner(spinner)
                state.setState(States.RESIZE)

    @staticmethod
    def exitCheck(action):
        # temporary code reduction, before utilising partial screen refresh
        # pygame.display.update()  # Redraw screen when no argument
        # pass (start_x, start_y, width, height) to redraw portion of screen
        if action.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

