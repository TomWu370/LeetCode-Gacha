from UI.Button.Button import Button
import pygame
from pygame.draw import rect


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
