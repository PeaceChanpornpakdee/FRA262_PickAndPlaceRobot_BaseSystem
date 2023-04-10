from components.shape import RoundRectangle
from components.color import Color

class TextBox():
    def __init__(self, canvas, x, y, text, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.textbox = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=("Inter-SemiBold", self.size))

    def activate(self, active_text, active_color):
        self.canvas.itemconfigure(self.textbox, text=active_text, fill=active_color)

    def deactivate(self, inactive_text, inactive_color):
        self.canvas.itemconfigure(self.textbox, text=inactive_text, fill=inactive_color)

    def hide(self):
        self.canvas.itemconfigure(self.textbox, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.textbox, state='normal')

    def change_text(self, text):
        self.canvas.itemconfigure(self.textbox, text=text)


class MessageBox():
    def __init__(self, canvas, x, y, text, color, direction):
        self.canvas = canvas
        self.text = text
        self.w = self.find_width()
        self.h = 20
        self.r = 6
        self.x = x - self.w
        self.y = y
        self.color = color
        self.direction = direction
        self.create()

    def find_width(self):
        if self.text == "Going Home":
            return 87
        if self.text == "Going to Pick":
            return 95
        if self.text == "Going to Place":
            return 100
        if self.text == "Laser On":
            return 70
        if self.text == "Gripper Pick":
            return 90
        if self.text == "Gripper Place":
            return 95
        if self.text == "Input x for Point Mode must be between -15.0 and 15.0":
            return 321
        if self.text == "Input y for Point Mode must be between -35.0 and 35.0":
            return 327
        return int(len(self.text) * 7.5)
    
    def create_tail(self):
        if self.direction == "NW":
            tail_points = (
                (self.x-4, self.y-4),
                (self.x+4, self.y),
                (self.x,   self.y+4)
            )
        elif self.direction == "NE":
            tail_points = (
                (self.w+self.x+4, self.y-4),
                (self.w+self.x-4, self.y),
                (self.w+self.x,   self.y+4)
            )
        elif self.direction == "SW":
            tail_points = (
                (self.x-4, self.h+self.y+4),
                (self.x+4, self.h+self.y),
                (self.x,   self.h+self.y-4)
            )
        elif self.direction == "SE":
            tail_points = (
                (self.w+self.x+4, self.h+self.y+4),
                (self.w+self.x-4, self.h+self.y),
                (self.w+self.x,   self.h+self.y-4)
            )
        self.tail = self.canvas.create_polygon(*tail_points, fill=self.color, outline="")

    def create(self):
        self.create_tail()
        self.rectangle_box = RoundRectangle(canvas=self.canvas, x=self.x, y=self.y, w=self.w, h=self.h, r=self.r, color=self.color)
        self.textbox = self.canvas.create_text((self.x+10,self.y+9), text=self.text, fill=Color.white, font=("Inter-SemiBold", 11), anchor="w")

    def delete(self):
        self.canvas.delete(self.navigator_laser)
        self.canvas.delete(self.tail)
        self.canvas.delete(self.navigator_top)
        self.canvas.delete(self.navigator_left)
        self.canvas.delete(self.navigator_right)