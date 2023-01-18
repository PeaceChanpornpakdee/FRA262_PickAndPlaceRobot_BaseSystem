import pygame
  
# Initializing imported module
pygame.init()
  
# Displaying a window
pygame.display.set_mode((750, 750))
  
# Creating a bool value which checks if game is running
running = True
  
# Keep game running till running is true
while running:
    # Check for event if user has pushed any event in queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False