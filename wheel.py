import pygame
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.backends.backend_agg as agg

matplotlib.use("Agg")
matplotlib.rcParams['font.size'] = 14.0


class Wheel:

    def __init__(self, decisions, weights):
        self.decisions = decisions
        self.weights = weights

        self.decision_ranges = {}
        self.initialiseRanges(weights)

    def initialiseRanges(self, weights):
        total_weight = sum(weights)

        for i in range(len(weights)):
            # the current choice's starting degree = the end degree of the last choice
            if i == 0:
                start = 0
            else:
                start = self.decision_ranges[i - 1]['end']
            end = start + (weights[i] / total_weight) * 360

            self.decision_ranges[i] = {"start": start, "end": end}
        return self.decision_ranges

    def createWheel(self, width, height):
        # create piechart
        plt.clf()
        fig, ax = plt.subplots(1, 1, figsize=(width, height))

        # radius of 1.5 fits the screen the best
        plt.pie(self.weights, labels=self.decisions, counterclock=False, radius=1.5, startangle=90, labeldistance=0.3,
                rotatelabels=True)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        raw_data = canvas.tostring_argb()

        size = canvas.get_width_height()

        image = pygame.image.frombuffer(raw_data, size, "ARGB")
        return image

    def getRanges(self):
        return self.decision_ranges
