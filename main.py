import pygame
from time import time
from readConfig import readScreenDefault, readSpinnerDefault, readCustomisationDefault, readRates
from programManager import Manager
from UI.Button import Button, CircleButton, RectangleButton
from UI.Text import Text, VariableText
from spinner import Spinner
from states import States, State
from wheel import Wheel

# Initialisation for pygame
pygame.init()
font = pygame.font.SysFont(None, 28)

# variable fetching/reading
name, easy, medium, hard, money = Manager.startUp()  # overhead of 2-3 seconds from leetcode api
aspect, text_gap, text_w, text_h = readScreenDefault()
max_v, min_v, decay, start_degree, clockwise, spinner_path = readSpinnerDefault()
screen_colours = readCustomisationDefault()
decisions, weights = readRates()


# useful object declaration
manager = Manager(current_degree=start_degree, current_velocity=0, current_state=States.MAIN, current_aspect=aspect)
wheel = Wheel(decisions, weights)
while True:
    # dynamic resolution here
    aspect = manager.getAspect()
    wheel_aspect = (aspect[0] * 0.7, aspect[1])

    screen = pygame.display.set_mode(aspect, pygame.RESIZABLE)
    wheel_surf = pygame.Surface(wheel_aspect)
    wheel_centre = wheel_surf.get_rect().center
    stat_surf = pygame.Surface(aspect)

    state = State(manager.getState())

    wheel_rect = wheel.createWheel(wheel_aspect[0] / 100, wheel_aspect[1] / 100)

    # 5 and 200 are micro adjustments, due to the matplotlib pie not being perfectly centered
    spinnerPos = (wheel_centre[0] - 5, wheel_centre[1] - 200)
    spinner = Spinner(wheel_surf, spinner_path, spinnerPos, max_v, min_v, decay, current_velocity=manager.getVelocity(),
                      starting_degree=manager.getDegree(), clockwise=clockwise)

    # initialise buttons
    Button.init()
    Text.init()

    username = VariableText(stat_surf, wheel_aspect[0], 1 * text_gap, text_w, text_h, name, font, "Username")
    easy_qu = VariableText(stat_surf, wheel_aspect[0], 2 * text_gap, text_w, text_h, easy, font, "Easy")
    medium_qu = VariableText(stat_surf, wheel_aspect[0], 3 * text_gap, text_w, text_h, medium, font, "Medium")
    hard_qu = VariableText(stat_surf, wheel_aspect[0], 4 * text_gap, text_w, text_h, hard, font, "Hard")
    currency = VariableText(stat_surf, wheel_aspect[0], 5 * text_gap, text_w, text_h, money, font, "Currency")
    texts = Text.getList()

    refreshButton = RectangleButton(stat_surf, wheel_aspect[0], 0, 100, 20, font, "Refresh",
                                       VariableText.processTexts, texts[1:])  # ignore username
    # + 15 on wheel_centre[0] is micro adjustment
    startButton = CircleButton(wheel_surf, (wheel_centre[0] + 15, wheel_centre[1]), 20, 0, font,
                                  [Spinner.spin, VariableText.processTexts], [spinner, texts[1:], state])
    buttons = Button.getList()

    while state.getState() != States.RESIZE:
        pygame.display.update()

        stat_surf.fill(screen_colours['stat_background'])

        # render and update spinner with current degree
        wheel_surf.blit(wheel_rect, (0, 0))
        spinner.drawSpinner()

        # render buttons
        manager.renderTexts(texts)
        manager.renderButtons(buttons)

        # Update screen
        screen.blit(stat_surf, (0, 0))
        screen.blit(wheel_surf, (0, 0))

        match state.getState():
            case States.SPIN:
                spinner.rotateSpinner()
                if spinner.isStop():
                    # change screen
                    state.setState(States.RESULT)

            case States.RESULT:
                degree = spinner.getDegree()
                for i in range(len(decisions)):
                    # if degree within range then announce result
                    if wheel.getRanges()[i]['start'] < degree < wheel.getRanges()[i]['end']:
                        # announce result
                        result = decisions[i]
                        manager.displayResult(result, font, screen, screen_colours['result_text'])
                        break

                    elif degree in {wheel.getRanges()[i]['start'], wheel.getRanges()[i]['end']}:
                        manager.displayResult('Spinning Again', font, screen, screen_colours['retry_text'])
                        time.sleep(1)
                        spinner.spin()
                        state.setState(States.SPIN)
                        break
            case States.INSUFFICIENT:
                # when not enough money to spin
                manager.displayResult("Not enough money", font, screen, screen_colours['insufficient_text'])

        manager.processEvents(screen, state, spinner)


# Issue/Improvement 1) ghost shadow on spinner

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
