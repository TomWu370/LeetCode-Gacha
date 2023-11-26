import pygame
from matplotlib import pyplot as plt
from pygame import gfxdraw
from PIL import Image, ImageDraw
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg


import pylab
import sys
import math
import database as db
import leetscore
import ui
from spinner import Spinner
from states import States, State


# api
# top bar showcasing currency
# database to record

def startUp():
    # get initial data
    username = leetscore.getUsername()
    data, gold = db.refresh()
    return username, data['easy'], data['medium'], data['hard'], gold


def getEvents():
    return pygame.event.get()


def processEvents():
    for event in getEvents():
        quit(event)


def quit(action):
    # temporary code reduction, before utilising partial screen refresh
    # pygame.display.update()  # Redraw screen when no argument
    # pass (start_x, start_y, width, height) to redraw portion of screen
    if action.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def renderButtons(objects):
    for button in objects:
        button.process()


def renderTexts(objects):
    for text in objects:
        text.process()


def displayresult(result, font, screen):
    textsurface = font.render(result, True, (0, 255, 0))
    textrect = textsurface.get_rect()
    textrect.center = screen.get_rect().center
    screen.blit(textsurface, textrect)


aspect = (1600, 900)
wheel_aspect = (aspect[0] * 0.7, aspect[1])
text_gap = 50
text_w = 100
text_h = 20
pygame.init()  # Initializing pygame
font = pygame.font.SysFont(None, 28)

screen = pygame.display.set_mode(aspect, pygame.RESIZABLE)
wheel_surf = pygame.Surface(wheel_aspect)
wheel_centre = wheel_surf.get_rect().center
stat_surf = pygame.Surface(aspect)

state = State()

decisions = ['choice1', 'choice2', 'choice3', 'choice4']
weights = [1,1,1,4]
num_decisions = len(decisions)

decision_ranges = {}
total_weight = sum(weights)

for i in range(len(weights)):
    # the current choice's starting degree = the end degree of the last choice
    if i == 0:
        start = 0
    else:
        start = decision_ranges[i - 1]['end']
    end = start + (weights[i]/total_weight) * 360

    decision_ranges[i] = {"start": start, "end": end}

##### create piechart

fig, ax = plt.subplots(1,1, figsize=(wheel_aspect[0]/100, wheel_aspect[1]/100))

# radius of 1.5 fits the screen the best
plt.pie(weights, labels=decisions, counterclock=False, radius=1.5, startangle=90,  labeldistance=0.7, rotatelabels=270)

ax = fig.gca()

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_argb()

size = canvas.get_width_height()

image = pygame.image.frombuffer(raw_data, size, "ARGB")

##### - convert into PyGame image -

# 5 and 200 are micro adjustments, due to the matplotlib pie not being perfectly centered
spinnerPos = (wheel_centre[0]-5, wheel_centre[1]-200)
spinner = Spinner(wheel_surf, "pointer.png", spinnerPos, 3, 1, 0.002)

name, easy, medium, hard, money = startUp()  # overhead of 2-3 seconds

username = ui.variableText(stat_surf, wheel_aspect[0], 1 * text_gap, text_w, text_h, leetscore.getUsername(), font, "Username")
easy_qu = ui.variableText(stat_surf, wheel_aspect[0], 2 * text_gap, text_w, text_h, easy, font, "Easy")
medium_qu = ui.variableText(stat_surf, wheel_aspect[0], 3 * text_gap, text_w, text_h, medium, font, "Medium")
hard_qu = ui.variableText(stat_surf, wheel_aspect[0], 4 * text_gap, text_w, text_h, hard, font, "Hard")
currency = ui.variableText(stat_surf, wheel_aspect[0], 5 * text_gap, text_w, text_h, money, font, "Currency")
texts = ui.Text.getList()


refreshButton = ui.RectangleButton(stat_surf, wheel_aspect[0], 0, 100, 20, font, "Refresh",
                                   ui.variableText.processTexts, texts[1:])  # ignore username
# + 15 on wheel_centre[0] is micro adjustment
startButton = ui.CircleButton(wheel_surf, (wheel_centre[0]+15, wheel_centre[1]), 20, 0, font,
                              [Spinner.spin,ui.variableText.processTexts], [spinner, texts[1:], state])
buttons = ui.Button.getList()

while True:
    pygame.display.update()

    stat_surf.fill((125, 255, 255))

    score = font.render("Score: " + str(money), False, (200, 0, 50))


    # update spinner with current degree
    wheel_surf.blit(image, (0,0))
    spinner.drawSpinner()

    # render buttons and screen
    renderTexts(texts)

    renderButtons(buttons)

    screen.blit(stat_surf, (0, 0))

    screen.blit(wheel_surf, (0, 0))


    match state.getState():
        case States.SPIN:
            spinner.rotateSpinner()
            if spinner.isStop():
                # announce result
                # state = RESULT  # change screen
                state.setState(States.RESULT)

        case States.RESULT:
            degree = spinner.getDegree()
            for i in range(num_decisions):
                # if degree within range then announce result
                if decision_ranges[i]['start'] < degree < decision_ranges[i]['end']:

                    result = decisions[i]
                    displayresult(result, font, screen)
                    break

                elif degree in {decision_ranges[i]['start'], decision_ranges[i]['end']}:
                    displayresult('Spinning Again', font, screen)
                    spinner.spin()
                    state.setState(States.SPIN)
                    break
        case States.INSUFFICIENT:
            # when not enough money to spin
            displayresult("Not enough money", font, screen)

    processEvents()

# To Do:
# 1) Update pointer.png to include button O
# 2) Add leetcode integration and database for currency O
# 3) Add respin logic O
# 4) when spinning disable respin O
# 5) Update ui to include values and username O
# 6) Update spinner,py to verify current currency amount before spinning, otherwise return insufficient balance O
# 7) To verify, modify database.py to return true or false, then add boolean check to spinner.py O
# 8) Modify main.py and spinner.py and ui.py to shift state changing to spinner.py spin(), O
#    then pass state object to spinner
# 9) separate screen and stat_surf O
# firstly create a large screen, then define wheel surface and stat surface separately O
# modify rectangular button class to not create new surface but rather print on existing surface like circular button O
# 10) update pie chart drawing method to use PIL image with degree based positioning and use image instead O
# 11) implement layer system to manage all the different layers/surfaces/images/attachments


# helpful snippets
# collision detection:
# for event in getEvents():
#     quit(event)
#     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#         # click on plate area
#         if pointer.get_rect().collidepoint(event.pos):
#             # Left mouse button. collide with area
#             # Check if the rect collides with the mouse pos.
#             print('Area clicked.')
#             print(event.pos)
#             print(pointer.get_rect())
#             break

# newVal = [name, easy, medium, hard, money] = startUp() this syntax could be used to convert multi value function
# into a list
