import random
import pygame
class Spinner():
    def __init__(self, screen, pointer_img, pointer_pos, max_velocity, min_velocity=0, decay=0.002, starting_degree=0):
        self.screen = screen
        self.pointer = pygame.image.load(pointer_img).convert_alpha() # Use convert_alpha to preserve transparency
        self.pointer_pos = pointer_pos  # Put it in the middle
        self.max_velocity = max_velocity
        self.min_velocity = min_velocity
        self.velocity = 0
        self.decay = decay # adjust this value so that it depends on number of decisions, 0.0002
        self.degree = starting_degree  # starting wheel degree
        self.blitted_rect = None

    def drawSpinner(self):
        self.screen.fill((255, 255, 255))  # Fill with white
        self.blitted_rect = self.screen.blit(self.pointer, self.pointer_pos)  # Put the spinner on the screen
        self.screen.blit(self.pointer, self.blitted_rect)


    def rotateSpinner(self):
        try:
            oldCenter = self.blitted_rect.center  # Find old center of spinner
            rotatedSurf = pygame.transform.rotate(self.pointer, self.degree)  # Rotate spinner by degree (0 at first)

            rotRect = rotatedSurf.get_rect()  # Get dimensions of rotated spinner
            rotRect.center = oldCenter  # Assign center of rotated spinner to center of pre-rotated

            self.screen.blit(rotatedSurf, rotRect)  # Put the rotated spinner on screen
        except AttributeError:
            self.drawSpinner()
            self.rotateSpinner()

    def isStop(self):
        if self.velocity > 0:
            self.degree = (self.degree - self.velocity) % 360  # decrease angle by velocity
            self.velocity -= self.decay
            return False
        else:
            self.velocity = 0
            return True  # change screen

    def spin(self):
        if self.velocity == 0:
            self.velocity = random.uniform(self.min_velocity, self.max_velocity)

    def getDegree(self):
        return self.degree