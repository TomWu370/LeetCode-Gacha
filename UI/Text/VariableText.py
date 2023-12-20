import pygame
from Database import Database

from UI.Text.Text import Text


class VariableText(Text):
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