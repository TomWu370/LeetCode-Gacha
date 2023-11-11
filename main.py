import pygame
from pygame import gfxdraw
import time
import sys
import random
import math
import database as db
import ui
from spinner import Spinner

# api
# top bar showcasing currency
# database to record

# STATES
MAIN = 0
RESULT = 1
RETRY = 2


def startUp():
    # get initial data
    money = db.getUsable()
    data = db.read()
    return money, data

def getEvents():
    return pygame.event.get()

def processEvents():
    for event in getEvents():
        quit(event)

def quit(action):
    # temporary code reduction, before utilising partial screen refresh
    pygame.display.update()  # Redraw screen when no argument
    # pass (start_x, start_y, width, height) to redraw portion of screen
    if action.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def renderButtons(buttons):
    for button in buttons:
        button.process()


def displayresult(result, font, screen):
    textsurface = font.render(result, True, (0, 255, 0))
    textrect = textsurface.get_rect()
    textrect.center = screen.get_rect().center
    screen.blit(textsurface, textrect)
    pygame.display.update()


pygame.init()  # Initializing pygame
font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((800, 800))

decisions = ['choice1', 'choice2']
degree = 0  # starting wheel degree
num_decisions = len(decisions)
splits = int(360 / num_decisions)
velocity = initial_velocity = random.uniform(0, 2)
decay = 0.0002  # adjust this value so that it depends on number of decisions, 0.0002

pointer = Spinner(screen, 2, 2)

money, data = startUp()
buttons = []
refreshButton = ui.RectangleButton(screen, 500, 280, 100, 20, font, "Refresh", ui.buttonAction)
startButton = ui.CircleButton(screen, 200, 200, 20, 0, font, Spinner.respin, pointer)
buttons.extend([refreshButton, startButton])

state = MAIN
while state == MAIN:
    pygame.display.update()
    pointer.drawSpinner()
    pygame.draw.circle(screen, (150, 50, 0), (200, 200), 200, 3)
    text = pygame.Surface((200, 200))
    text.fill((125, 255, 255))
    score = font.render("Score: " + str(money), False, (200, 0, 50))
    screen.blit(text, (500, 300))
    screen.blit(score, (500, 300))

    # render buttons
    renderButtons(buttons)

    # render separation line on chart
    for i in range(num_decisions):
        # draw separation line for each choice
        gfxdraw.pie(screen, 200, 200, 200, i * splits, splits, (0, 0, 0))

    # render decision text
    for i in range(0, num_decisions):
        # for each decision place the corresponding text on screen
        textChoice = font.render(decisions[i], False, (0, 0, 0))
        textWidth = textChoice.get_rect().width
        textHeight = textChoice.get_rect().height
        i += i + 1

        textChoice = pygame.transform.rotate(textChoice, (i - (2 * i)) * (360 / (num_decisions * 2)))
        textWidth = textChoice.get_rect().width
        textHeight = textChoice.get_rect().height
        # (200 - 100) controls how close  text is to center, 0 = very close, >100 = away
        screen.blit(textChoice, (
            (200 - (textWidth / 2))
            + ((200 - 100) * math.cos(((i * (360 / (num_decisions * 2)))) * (math.pi / 180))),
            (200 - (textHeight / 2))
            + ((200 - 100) * math.sin(((i * (360 / (num_decisions * 2)))) * (math.pi / 180)))
        ))
        textChoice = ''
    pointer.rotateSpinner()

    if pointer.isStop():
        # announce result
        state = RESULT # change screen

    while state == RESULT:
        renderButtons(buttons)
        processEvents()
        degree = pointer.getDegree()
        for i in range(num_decisions):
            # if degree within range then announce result
            if i * (360 / num_decisions) < degree < (i + 1) * (360 / num_decisions):
                state = RETRY
                print(f'i:', i)
                result = decisions[i]
                displayresult(result, font, screen)
                break

            elif degree % (360 / num_decisions) == 0:
                displayresult('Spinning Again', font, screen)
                print('on the line')

                state = MAIN
                velocity = random.uniform(0, 1.5)
                break

    while state == RETRY:
        renderButtons(buttons)
        if pointer.velocity > 0:
            # button for respin is pressed so velocity changed, therefore change state
            state = MAIN
            break

        for event in getEvents():

            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     # click on plate area
            #     if pointer.get_rect().collidepoint(event.pos):
            #         # Left mouse button. collide with area
            #         # Check if the rect collides with the mouse pos.
            #         print('Area clicked.')
            #         print(event.pos)
            #         print(pointer.get_rect())
            #         break
            quit(event)

    processEvents()

# To Do:
# 1) Update pointer.png to include button
# 2) Add leetcode integration and database for currency
# 3) Add respin logic
# 4) when spinning disable respin
