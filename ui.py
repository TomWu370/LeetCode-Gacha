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
    def init(cls):
        cls.buttons = []

    @classmethod
    def getList(cls):
        return cls.buttons


class RectangleButton(Button):
    def __init__(self, screen, x, y, width, height, font, buttonText=None, onclickFunction=None, functionArgument=None,
                 onePress=False):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.onclickFunction = onclickFunction
        self.functionArgument = functionArgument
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonDim = None

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        if buttonText:
            self.textSurf = font.render(buttonText, True, (20, 20, 20))

    def process(self):
        mousePos = pygame.mouse.get_pos()

        self.buttonDim = rect(self.screen, self.fillColors['normal'], self.rect, 0)

        if self.buttonDim.collidepoint(mousePos):
            self.buttonDim = rect(self.screen, self.fillColors['hover'], self.rect, 0)
            if not pygame.mouse.get_pressed()[0]:
                self.alreadyPressed = False

            else:
                self.buttonDim = rect(self.screen, self.fillColors['pressed'], self.rect, 0)
                if self.onePress:
                    self.onclickFunction(self.functionArgument)
                elif not self.alreadyPressed:
                    self.alreadyPressed = True
                    self.onclickFunction(self.functionArgument)
        if self.textSurf:
            textrect = self.textSurf.get_rect()
            textrect.center = self.rect.center
            self.screen.blit(self.textSurf, textrect)


class CircleButton(Button):
    def __init__(self, screen, center, radius, width, font, onclickFunction=None, functionArgument=None,
                 onePress=False):
        super().__init__()
        self.screen = screen
        self.center = center
        self.radius = radius
        self.width = width
        self.font = font
        # specialised for Spin button
        self.onclickFunction = onclickFunction
        self.spin = onclickFunction[0]
        self.refresh = onclickFunction[1]

        self.functionArgument = functionArgument
        self.spinner = functionArgument[0]
        self.texts = functionArgument[1]
        self.state = functionArgument[2]

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

        if self.buttonDim.collidepoint(mousePos) and V.distance_to(V(self.buttonDim.center),
                                                                   V(mousePos)) <= self.radius:
            self.buttonDim = circle(self.screen, self.fillColors['hover'], self.center, self.radius, self.width)
            if not pygame.mouse.get_pressed()[0]:
                self.alreadyPressed = False

            else:
                self.buttonDim = circle(self.screen, self.fillColors['pressed'], self.center, self.radius, self.width)

                if self.onePress ^ (not self.alreadyPressed):  # xor between the 2 condition
                    if self.state.getState() == States.SPIN:  # check if spinner is already spinning
                        if not self.alreadyPressed: self.alreadyPressed = True
                    elif not database.spend():
                        self.state.setState(States.INSUFFICIENT)
                    else:
                        if not self.alreadyPressed: self.alreadyPressed = True
                        self.spin(self.spinner)
                        self.refresh(self.texts)
                        self.state.setState(States.SPIN)



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


class variableText(Text):
    def __init__(self, screen, x, y, width, height, variable, font, buttonText=None):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.variable = variable
        self.font = font
        self.buttonText = buttonText if buttonText else ""
        self.textSurf = self.font.render((self.buttonText + ": " + str(self.variable)), True, (20, 20, 20))

    def process(self):
        textrect = self.textSurf.get_rect()
        textrect.topleft = self.rect.topleft
        self.screen.blit(self.textSurf, textrect)

    def updateVariable(self, newValue):
        self.variable = newValue
        self.textSurf = self.font.render((self.buttonText + ": " + str(newValue)), True, (20, 20, 20))

    @staticmethod
    def processTexts(variables):
        data, usable = database.refresh()
        data = list(data.values())
        data.append(usable)
        for i in range(len(variables)):
            variables[i].updateVariable(data[i])


def buttonAction(*args):
    print(database.read())
