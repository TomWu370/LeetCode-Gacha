from UI.Button.Button import Button
import pygame
from pygame.draw import circle
from states import States
import database


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

