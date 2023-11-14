from abc import ABC, abstractmethod
import pygame
from pygame import Vector2 as V
from pygame.draw import rect, circle
from states import States
import database


class Button(ABC):
    buttons = []
    @abstractmethod
    def __init__(self):
        Button.buttons.append(self)
    @abstractmethod
    def process(self):
        pass

    @classmethod
    def getList(cls):
        return cls.buttons
class RectangleButton(Button):
    def __init__(self, screen, x, y, width, height, font, buttonText=None, onclickFunction=None, functionArgument=None, onePress=False):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(x,y, width, height)
        self.onclickFunction = onclickFunction
        self.functionArgument = functionArgument
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonDim = None

        self.fillColors = {
            'normal': '#333333',
            'hover': '#666666',
            'pressed': '#333333',
        }

        #self.buttonSurface = pygame.Surface((self.width, self.height))
        #self.buttonDim = rect(self.x, self.y, self.width, self.height)
        if buttonText:
            self.textSurf = font.render(buttonText, True, (20, 20, 20))

    def process(self):
        mousePos = pygame.mouse.get_pos()

        self.buttonDim = rect(self.screen, self.fillColors['normal'],self.rect, 0)

        if self.buttonDim.collidepoint(mousePos):
            print(self.buttonDim)
            self.buttonDim = rect(self.screen, self.fillColors['hover'],self.rect, 0)
            if not pygame.mouse.get_pressed()[0]:
                self.alreadyPressed = False

            else:
                self.buttonDim = rect(self.screen, self.fillColors['pressed'],self.rect, 0)
                if self.onePress:
                    self.onclickFunction(self.functionArgument)
                elif not self.alreadyPressed:
                    self.onclickFunction(self.functionArgument)
                    self.alreadyPressed = True
        if self.textSurf:
            textrect = self.textSurf.get_rect()
            textrect.center = self.rect.center
            self.screen.blit(self.textSurf, textrect)
        # self.buttonSurface.blit(self.buttonSurf, [
        #     self.buttonDim.width / 2 - self.buttonSurf.get_rect().width / 2,
        #     self.buttonDim.height / 2 - self.buttonSurf.get_rect().height / 2
        # ])
        #self.screen.blit(self.buttonSurface, self.buttonDim)

class CircleButton(Button):
    def __init__(self, screen, x, y, radius, width, font, onclickFunction=None, functionArgument=None, onePress=False):
        super().__init__()
        self.screen = screen
        self.center = (x, y)
        self.radius = radius
        self.width = width
        self.font = font
        self.onclickFunction = onclickFunction
        self.functionArgument = functionArgument
        # specialised for Retry button
        self.spinner = functionArgument[0]
        self.state = functionArgument[1]
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#666666',
            'hover': '#333333',
            'pressed': '#111111',
        }

        self.buttonDim = circle(screen, self.fillColors['normal'], self.center, radius, width)

    def process(self):
        mousePos = pygame.mouse.get_pos()

        self.buttonDim = circle(self.screen, self.fillColors['normal'], self.center, self.radius, self.width)

        if self.buttonDim.collidepoint(mousePos) and V.distance_to(V(self.buttonDim.center), V(mousePos)) <= self.radius:
            self.buttonDim = circle(self.screen, self.fillColors['hover'], self.center, self.radius, self.width)
            if not pygame.mouse.get_pressed()[0]:
                self.alreadyPressed = False

            else:
                self.buttonDim = circle(self.screen, self.fillColors['pressed'], self.center, self.radius, self.width)
                if self.onePress:
                    self.onclickFunction(self.spinner)
                    self.state.setState(States.SPIN)

                elif not self.alreadyPressed:
                    self.onclickFunction(self.spinner)
                    self.state.setState(States.SPIN)
                    self.alreadyPressed = True


def buttonAction(*args):
    print(database.read())