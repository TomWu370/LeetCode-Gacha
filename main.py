import pygame
from pygame import gfxdraw
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
pygame.init()  # Initializing pygame
font = pygame.font.SysFont(None, 28)

screen = pygame.display.set_mode(aspect, pygame.RESIZABLE)
wheel_surf = pygame.Surface(wheel_aspect)
stat_surf = pygame.Surface(aspect)

state = State()

decisions = ['choice1', 'choice2', 'choice3', 'choice4', 'choice5']
num_decisions = len(decisions)
splits = int(360 / num_decisions)
wheel_centre = 400
wheel_radius = wheel_centre
spinnerPos = (wheel_centre - 20, wheel_centre - 200)
spinner = Spinner(wheel_surf, "pointer.png", spinnerPos, 1, 0)

name, easy, medium, hard, money = startUp()  # overhead of 2-3 seconds

username = ui.variableText(stat_surf, wheel_aspect[0], 50, 100, 20, leetscore.getUsername(), font, "Username")
easy_qu = ui.variableText(stat_surf, wheel_aspect[0], 100, 100, 20, easy, font, "Easy")
medium_qu = ui.variableText(stat_surf, wheel_aspect[0], 150, 100, 20, medium, font, "Medium")
hard_qu = ui.variableText(stat_surf, wheel_aspect[0], 200, 100, 20, hard, font, "Hard")
currency = ui.variableText(stat_surf, wheel_aspect[0], 250, 100, 20, money, font, "Currency")
texts = ui.Text.getList()

# Text row, text + variable
# each frame update text, however not fetching otherwise it'd be too slow
# self variable, when updated, these variables are updated as well
# pass text list as object like start button, then update the variables
# process method would just be displaying and blitting

refreshButton = ui.RectangleButton(stat_surf, wheel_aspect[0], 0, 100, 20, font, "Refresh",
                                   ui.variableText.processTexts, texts[1:])  # ignore username
startButton = ui.CircleButton(wheel_surf, wheel_centre, wheel_centre, 20, 0, font,
                              [Spinner.spin,ui.variableText.processTexts], [spinner, texts[1:], state])
buttons = ui.Button.getList()

while True:
    pygame.display.update()

    wheel_surf.fill((255, 255, 255))  # Fill 'screen' with white
    stat_surf.fill((125, 255, 255))

    pygame.draw.circle(wheel_surf, (150, 50, 0), (wheel_centre, wheel_radius), wheel_radius, 3)
    score = font.render("Score: " + str(money), False, (200, 0, 50))

    # render separation line on chart
    for i in range(num_decisions):
        # draw separation line for each choice
        gfxdraw.pie(wheel_surf, wheel_centre, wheel_radius, wheel_radius, i * splits, splits, (0, 0, 0))

    # render decision text
    for i in range(0, num_decisions):
        # for each decision place the corresponding text on screen
        text = font.render(decisions[i], False, (0, 0, 0))
        # generate i to be descending from list of odd numbers, so length of 3 would be 3,1,-1
        i = 2 * (num_decisions - i - 2) + 1  # move the first element back 2 slices, counterclockwise

        if i <= (num_decisions / 2):
            textChoice = pygame.transform.rotate(text, (-i) * (360 / (num_decisions * 2)))
        else:
            textChoice = pygame.transform.rotate(text, (num_decisions - i) * (360 / (num_decisions * 2)))

        textWidth = textChoice.get_rect().width
        textHeight = textChoice.get_rect().height
        # (200 - 100) controls how close  text is to center, 0 = very close, >100 = away
        wheel_surf.blit(textChoice, (
            (wheel_centre - (textWidth / 2))
            + ((wheel_centre - 100) * math.cos((i * (360 / (num_decisions * 2))) * (math.pi / 180))),
            (wheel_centre - (textHeight / 2))
            + ((wheel_centre - 100) * math.sin((i * (360 / (num_decisions * 2))) * (math.pi / 180)))
        ))

    # update spinner with current degree
    spinner.drawSpinner()

    # render buttons and screen
    renderButtons(buttons)
    renderTexts(texts)
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
                if i * (360 / num_decisions) < degree < (i + 1) * (360 / num_decisions):

                    #print(f'i:', i)
                    result = decisions[i]
                    displayresult(result, font, screen)
                    # state.setState(States.MAIN)
                    break

                elif degree % (360 / num_decisions) == 0:
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
# 5) Update ui to include values and username
# 6) Update spinner,py to verify current currency amount before spinning, otherwise return insufficient balance
# 7) To verify, modify database.py to return true or false, then add boolean check to spinner.py
# 8) Modify main.py and spinner.py and ui.py to shift state changing to spinner.py spin(),
#    then pass state object to spinner
# 9) separate screen and stat_surf
# firstly create a large screen, then define wheel surface and stat surface separately
# modify rectangular button class to not create new surface but rather print on existing surface like circular button


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
