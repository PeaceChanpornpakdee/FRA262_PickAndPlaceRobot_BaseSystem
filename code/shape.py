import pygame

class Rectangle:
    def __init__(self, screen, color, x, y, w, h):
        self.screen = screen
        self.color = color
        self.x = x # Center x
        self.y = y # Center y
        self.w = w # Width
        self.h = h # Height

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))


class Circle:
    def __init__(self, screen, color, x, y, r):
        self.screen = screen
        self.color = color
        self.x = x # Center x
        self.y = y # Center y
        self.r = r # Radius

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)




