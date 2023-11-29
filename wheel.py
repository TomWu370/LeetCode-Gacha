import pygame
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg


class Wheel:

    def __init__(self, decisions, weights):
        self.decisions = ['choice1', 'choice2', 'choice3', 'choice4']
        self.weights = [1, 1, 1, 4]

        self.decision_ranges = self.initialiseRanges(weights)

    def initialiseRanges(self, weights):
        decision_ranges = {}
        total_weight = sum(weights)

        for i in range(len(weights)):
            # the current choice's starting degree = the end degree of the last choice
            if i == 0:
                start = 0
            else:
                start = decision_ranges[i - 1]['end']
            end = start + (weights[i] / total_weight) * 360

            decision_ranges[i] = {"start": start, "end": end}
        return decision_ranges

    def createWheel(self, width, height):
        ##### create piechart
        plt.clf()
        fig, ax = plt.subplots(1, 1, figsize=(width, height))

        # radius of 1.5 fits the screen the best
        plt.pie(self.weights, labels=self.decisions, counterclock=False, radius=1.5, startangle=90, labeldistance=0.7,
                rotatelabels=270)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        raw_data = canvas.tostring_argb()

        size = canvas.get_width_height()

        image = pygame.image.frombuffer(raw_data, size, "ARGB")
        return image
