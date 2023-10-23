import pygame
from pygame import gfxdraw
import time
import sys
import random
import math


def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


pygame.init()  # Initializing pygame
font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((400, 400))
decisions = ['choice1', 'choice2']
degree = 0  # starting wheel degree
num_decisions = len(decisions)
splits = int(360 / num_decisions)
velocity = initial_velocity = random.uniform(0, 2)
decay = 0.0002 # adjust this value so that it depends on number of decisions


while True:
    pygame.display.flip()
    screen.fill([255, 255, 255])  # Fill with white

    plate = pygame.Surface((100, 100))  # Creating surface for the spinner
    plate.fill((255, 255, 255))  # White fill for the surface
    plate.set_colorkey((255, 255, 255))  # Colorkey out the white fill
    plate = pygame.image.load('pointer.png').convert_alpha()  # Use convert_alpha to preserve transparency
    pointerPos = 180, 10  # Put it in the middle
    blittedRect = screen.blit(plate, pointerPos)  # Put the spinner on the screen

    screen.fill([255, 255, 255])  # Re-draw screen
    pygame.draw.circle(screen, (0, 0, 0), (200, 200), 200, 3)

    for i in range(num_decisions):
        # draw separation line for each choice
        gfxdraw.pie(screen, 200, 200, 200, i * splits, splits, (0, 0, 0))

    for i in range(0, num_decisions):
        # for each decision place the corresponding text on screen
        textChoice = font.render(decisions[i], False, (0, 0, 0))
        textWidth = textChoice.get_rect().width
        textHeight = textChoice.get_rect().height
        i += i + 1

        textChoice = pygame.transform.rotate(textChoice, (i - (2 * i)) * (360 / (num_decisions * 2)))
        textWidth = textChoice.get_rect().width
        textHeight = textChoice.get_rect().height
        screen.blit(textChoice, (
            (200 - (textWidth / 2))
            + ((200 - 100) * math.cos(((i * (360 / (num_decisions * 2)))) * (math.pi/180))),
            (200 - (textHeight / 2))
            + ((200 - 100) * math.sin(((i * (360 / (num_decisions * 2)))) * (math.pi/180)))
        )
                    )
        textChoice = ''
    oldCenter = blittedRect.center  # Find old center of spinner

    rotatedSurf = pygame.transform.rotate(plate, degree)  # Rotate spinner by degree (0 at first)

    rotRect = rotatedSurf.get_rect()  # Get dimensions of rotated spinner
    rotRect.center = oldCenter  # Assign center of rotated spinner to center of pre-rotated

    screen.blit(rotatedSurf, rotRect)  # Put the rotated spinner on screen

    if velocity > 0:
        degree -= velocity  # decrease angle by velocity
        velocity -= decay
    else:
        velocity = 0
        # announce result

    pygame.display.flip()  # Redraw screen

    quit()
