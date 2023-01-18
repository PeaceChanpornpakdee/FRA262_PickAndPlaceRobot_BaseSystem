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
        pygame.draw.rect(self.screen, self.color, (self.x-self.w/2, self.y-self.h/2, self.w, self.h))


class Circle:
    def __init__(self, screen, color, x, y, r):
        self.screen = screen
        self.color = color
        self.x = x # Center x
        self.y = y # Center y
        self.r = r # Radius

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class RoundedRectangle:
    def __init__(self, screen, color, x, y, w, h, r):
        self.screen = screen
        self.color = color
        self.x = x # Center x
        self.y = y # Center y
        self.w = w # Width
        self.h = h # Height
        self.r = r # Corner radius

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x-self.w/2, self.y-self.h/2+self.r, self.w, self.h-2*self.r))
        pygame.draw.rect(self.screen, self.color, (self.x-self.w/2+self.r, self.y-self.h/2, self.w-2*self.r, self.h))
        # pygame.draw.rect(self.screen, self.color, (self.x-self.w/2, self.y-self.h/2+self.r, self.w, self.h-2*self.r))
        # pygame.draw.rect(self.screen, self.color, (self.x-self.w/2+self.r, self.y-self.h/2+self.r, self.w-2*self.r, self.h-2*self.r))
        pygame.draw.circle(self.screen, self.color, (self.x+self.w/2-self.r, self.y+self.h/2-self.r), self.r)
        pygame.draw.circle(self.screen, self.color, (self.x-self.w/2+self.r, self.y+self.h/2-self.r), self.r)
        pygame.draw.circle(self.screen, self.color, (self.x+self.w/2-self.r, self.y-self.h/2+self.r), self.r)
        pygame.draw.circle(self.screen, self.color, (self.x-self.w/2+self.r, self.y-self.h/2+self.r), self.r)
        