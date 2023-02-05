from shape import *
from color import Color

class Component:
    def __init__(self, screen):
        self.screen = screen 
        self.background = Rectangle (screen, Color.darkgray,   360, 360, 720, 720)
        self.frame_2 = RoundedRectangle (screen, Color.white,   510, 360, 360, 660, 20)
        self.rec_1  = Rectangle (screen, Color.red,   200, 200, 50, 100)
        self.cir_1  = Circle    (screen, Color.green, 0, 0, 25)
        self.cir_2  = Circle    (screen, Color.green, 400, 400, 100)
        self.rrec_1 = RoundedRectangle (screen, Color.blue, 200, 200, 50, 100, 10)

    def display(self):
        self.background.draw()
        self.frame_2.draw()
        # self.rec_1.draw()
        # self.cir_1.draw()
        # self.cir_2.draw()
        # self.rrec_1.draw()
        
