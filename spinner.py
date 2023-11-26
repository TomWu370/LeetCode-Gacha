import random
import pygame


class Spinner:
    def __init__(self, screen, pointer_img, pointer_pos, max_velocity, min_velocity=0, current_velocity=None, decay=0.002, starting_degree=0, clockwise=True):
        self.screen = screen
        self.pointer = pygame.image.load(pointer_img).convert_alpha()  # Use convert_alpha to preserve transparency
        self.pointer_pos = pointer_pos  # Put it in the middle
        self.max_velocity = max_velocity
        self.min_velocity = min_velocity
        self.velocity = 0 if not current_velocity else current_velocity
        self.decay = decay  # adjust this value so that it depends on number of decisions, 0.0002
        self.degree = starting_degree  # starting wheel degree
        self.spinner_rect = self.screen.blit(self.pointer, self.pointer_pos)
        self.clockwise = -1 if clockwise else 1


    def drawSpinner(self):
        rotated_surf = pygame.transform.rotate(self.pointer, self.clockwise*self.degree)  # Rotate spinner by degree (0 by default)
        rot_rect = rotated_surf.get_rect(center=self.spinner_rect.center)  # Get dimensions of rotated spinner
        self.screen.blit(rotated_surf, rot_rect)  # Put the rotated spinner on screen


    def rotateSpinner(self):
        self.degree = (self.degree + self.velocity) % 360.0  # decrease angle by velocity
        self.velocity -= self.decay

    def isStop(self):
        if self.velocity > 0:
            return False
        else:
            self.velocity = 0
            return True  # change screen

    def spin(self):
        if self.velocity == 0:
            self.velocity = random.uniform(self.min_velocity, self.max_velocity)

    def getDegree(self):
        return self.degree

    def getVelocity(self):
        return self.velocity
