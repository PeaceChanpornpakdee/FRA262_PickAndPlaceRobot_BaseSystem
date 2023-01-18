from shape import *
from color import Color

class Component:
    def __init__(self, screen):
        self.screen = screen 
        self.rec_1  = Rectangle (screen, Color.red,   200, 200, 50, 100)
        self.cir_1  = Circle    (screen, Color.green, 0, 0, 25)
        self.rrec_1 = RoundedRectangle (screen, Color.blue, 200, 200, 50, 100, 10)

    def display(self):
        self.rec_1.draw()
        self.cir_1.draw()
        self.rrec_1.draw()
        
