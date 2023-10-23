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
degree = 0  # starting wheel degree
initial_velocity = random.randint(100, 200)  # adjust the values to that it depends on number of results

while True:
    pygame.display.flip()
    screen.fill([255, 255, 255])
