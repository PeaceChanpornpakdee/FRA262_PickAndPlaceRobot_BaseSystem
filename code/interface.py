import pygame
from component import *
from color import Color

# Initialize imported module
pygame.init()
  
# Displaying a window
screen = pygame.display.set_mode((750, 750))

#Preparing components
component = Component(screen)
  
# Create a bool value which checks if game is running
running = True
  
# Keep game running until running is true
while running:
    # Check for event if user has pushed any event in queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    component.rec_1.draw()

    pygame.display.update()