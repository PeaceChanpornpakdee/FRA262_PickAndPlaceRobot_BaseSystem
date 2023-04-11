from components.shape import RoundRectangle, Polygon
from components.color import Color

class TextBox():
    def __init__(self, canvas, x, y, text, size, color, anchor=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.textbox = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=("Inter-SemiBold", self.size))
        if anchor != None:
            self.canvas.itemconfigure(self.textbox, anchor=anchor)

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
        self.text = text

    def move_to(self, x, y):
        self.canvas.move(self.textbox, x-self.x, y-self.y)
        self.x = x
        self.y = y


class MessageBox():
    def __init__(self, canvas, x, y, text, color, direction):
        self.canvas = canvas
        self.text = text
        self.original_x = x
        self.y = y
        self.find_width()
        self.h = 20
        self.r = 6
        self.color = color
        self.direction = direction
        self.tail_points = {}
        self.tail_points["NW"] = ((self.x-4, self.y-4), (self.x+5, self.y), (self.x+1, self.y+4))
        self.tail_points["NE"] = ((self.w+self.x+4, self.y-4), (self.w+self.x-5, self.y), (self.w+self.x-1, self.y+4))
        self.tail_points["SW"] = ((self.x-4, self.h+self.y+4), (self.x+5, self.h+self.y), (self.x+1, self.h+self.y-4))
        self.tail_points["SE"] = ((self.w+self.x+4, self.h+self.y+4), (self.w+self.x-5, self.h+self.y), (self.w+self.x-1, self.h+self.y-4))
        self.tail = Polygon(canvas=self.canvas, points=self.tail_points[self.direction], color=self.color)
        self.rectangle_box = RoundRectangle(canvas=self.canvas, x=self.x, y=self.y, w=self.w, h=self.h, r=self.r, color=self.color)
        self.textbox = TextBox(canvas=self.canvas, x=self.x+10, y=self.y+9, text=self.text, size=11, color=Color.white, anchor="w")
        
    def hide(self):
        self.tail.hide()
        self.rectangle_box.hide()
        self.textbox.hide()

    def show(self):
        self.tail.show()
        self.rectangle_box.show()
        self.textbox.show()

    def change_text(self, text):
        self.textbox.change_text(text)
        self.text = text
        self.find_width()
        self.rectangle_box.resize(w=self.w, h=self.h)
        self.move_to(self.x, self.y)

    def move_to(self, x, y):
        self.textbox.move_to(x+10, y+9)
        self.rectangle_box.move_to(x, y)

    def find_width(self):
        if self.text == "Going Home":
            self.w = 87
        elif self.text == "Going to Pick":
            self.w = 95
        elif self.text == "Going to Place":
            self.w = 100
        elif self.text == "Laser On":
            self.w = 70
        elif self.text == "Gripper Pick":
            self.w = 90
        elif self.text == "Gripper Place":
            self.w = 95
        elif self.text == Error.code_1:
            self.w = 228
        elif self.text == Error.code_2:
            self.w = 266
        elif self.text == Error.code_3:
            self.w = 260
        elif self.text == Error.code_4x:
            self.w = 321
        elif self.text == Error.code_4y:
            self.w = 327
        else:
            self.w = int(len(self.text) * 7.5)
        self.x = self.original_x - self.w

    # def create(self):
    #     self.create_tail()
    #     self.rectangle_box = RoundRectangle(canvas=self.canvas, x=self.x, y=self.y, w=self.w, h=self.h, r=self.r, color=self.color)
    #     self.textbox = self.canvas.create_text((self.x+10,self.y+9), text=self.text, fill=Color.white, font=("Inter-SemiBold", 11), anchor="w")

    # def delete(self):
    #     self.canvas.delete(self.navigator_laser)
    #     self.canvas.delete(self.tail)
    #     self.canvas.delete(self.navigator_top)
    #     self.canvas.delete(self.navigator_left)
    #     self.canvas.delete(self.navigator_right)

class Error:
    code_1  = "Input for Point Mode cannot be empty"
    code_2  = "Input for Point Mode cannot have 2 or more ."
    code_3  = "Input for Point Mode cannot have character"
    code_4x = "Input x for Point Mode must be between -15.0 and 15.0"
    code_4y = "Input y for Point Mode must be between -35.0 and 35.0"
