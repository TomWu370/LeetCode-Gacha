import pygame
from pygame import gfxdraw
import sys
import math
import database as db
import ui
from spinner import Spinner
from states import States, State


# api
# top bar showcasing currency
# database to record


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
screen = pygame.display.set_mode((1600, 900),pygame.RESIZABLE)
wheel_surf = pygame.Surface((500,500))
stat_surf = pygame.Surface((500, 500))

state = State()

decisions = ['choice1', 'choice2']
num_decisions = len(decisions)
splits = int(360 / num_decisions)

spinnerPos = (180, 10)
spinner = Spinner(wheel_surf, "pointer.png", spinnerPos, 2, 2)

money, data = startUp()
stat_rect = stat_surf.get_rect()
stat_rect.x, stat_rect.y = 600, 100
stat_rect.width, stat_rect.height = 100, 20
refreshButton = ui.RectangleButton(stat_surf, stat_surf.get_rect(),100, 20, font, "Refresh", ui.buttonAction)
startButton = ui.CircleButton(wheel_surf, 200, 200, 20, 0, font, Spinner.spin, [spinner, state])
buttons = ui.Button.getList()

while True:
    pygame.display.update()
    screen.fill((255,255,255))
    wheel_surf.fill((255, 255, 255))  # Fill 'screen' with white
    pygame.draw.circle(wheel_surf, (150, 50, 0), (200, 200), 200, 3)
    stat_surf.fill((125, 255, 255))
    score = font.render("Score: " + str(money), False, (200, 0, 50))


    # render separation line on chart
    for i in range(num_decisions):
        # draw separation line for each choice
        gfxdraw.pie(wheel_surf, 200, 200, 200, i * splits, splits, (0, 0, 0))

    # render decision text
    for i in range(0, num_decisions):
        # for each decision place the corresponding text on screen
        text = font.render(decisions[i], False, (0, 0, 0))
        i += i + 1

        textChoice = pygame.transform.rotate(text, (i - (2 * i)) * (360 / (num_decisions * 2)))
        textWidth = textChoice.get_rect().width
        textHeight = textChoice.get_rect().height
        # (200 - 100) controls how close  text is to center, 0 = very close, >100 = away
        wheel_surf.blit(textChoice, (
            (200 - (textWidth / 2))
            + ((200 - 100) * math.cos(((i * (360 / (num_decisions * 2)))) * (math.pi / 180))),
            (200 - (textHeight / 2))
            + ((200 - 100) * math.sin(((i * (360 / (num_decisions * 2)))) * (math.pi / 180)))
        ))

    # render buttons
    renderButtons(buttons)

    # update spinner with current degree
    spinner.drawSpinner()

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
                    print(f'i:', i)
                    result = decisions[i]
                    displayresult(result, font, screen)
                    state.setState(States.MAIN)
                    break

                elif degree % (360 / num_decisions) == 0:
                    displayresult('Spinning Again', font, screen)
                    print('on the line')
                    spinner.spin()
                    state.setState(States.SPIN)
                    break
    screen.blit(wheel_surf, (0,0))
    screen.blit(stat_surf, (600, 100))
    #screen.blit(refreshButton.buttonSurface, (500,280))
    screen.blit(score, (500, 300))
    #renderButtons(buttons)
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
