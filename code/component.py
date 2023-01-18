from shape import *
from color import Color

class Component:
    def __init__(self, screen):
        self.rec_1 = Rectangle(screen, Color.red, 30, 40, 50, 100)