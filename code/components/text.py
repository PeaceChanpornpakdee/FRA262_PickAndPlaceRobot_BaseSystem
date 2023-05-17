import platform
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
        self.os = platform.platform()[0].upper()
        if self.os == 'M': #Mac
            self.textbox = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=("Inter-SemiBold", self.size))
        elif self.os == 'W': #Windows  
            self.textbox = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=("Inter SemiBold", self.size))
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
    def __init__(self, canvas, x, y, text, color, direction, align, size):
        self.canvas = canvas
        self.text = text
        self.align = align
        self.size = size
        self.find_width()
        self.h = 20
        self.x = x
        self.y = y
        self.r = 6
        self.color = color
        self.direction = direction
        self.tail_points = {}
        self.generate_tail_points()
        self.tail = Polygon(canvas=self.canvas, points=self.tail_points[self.direction], color=self.color)
        self.rectangle_box = RoundRectangle(canvas=self.canvas, x=self.x, y=self.y, w=self.w, h=self.h, r=self.r, color=self.color)
        self.textbox = TextBox(canvas=self.canvas, x=self.x+10, y=self.y+9, text=self.text, size=self.size, color=Color.white, anchor="w")
        
    def generate_tail_points(self):
        offset = 0
        if self.align == "Right":
            offset = -self.w
        self.tail_points["C"]  = ((offset+self.x, self.y), (offset+self.x, self.y), (offset+self.x, self.y))
        self.tail_points["NW"] = ((offset+self.x-4, self.y-4),               (offset+self.x+5, self.y),               (offset+self.x+1, self.y+4))
        self.tail_points["NE"] = ((offset+self.w+self.x+4, self.y-4),        (offset+self.w+self.x-5, self.y),        (offset+self.w+self.x-1, self.y+4))
        self.tail_points["SW"] = ((offset+self.x-4, self.h+self.y+4),        (offset+self.x+5, self.h+self.y),        (offset+self.x+1, self.h+self.y-4))
        self.tail_points["SE"] = ((offset+self.w+self.x+4, self.h+self.y+4), (offset+self.w+self.x-5, self.h+self.y), (offset+self.w+self.x-1, self.h+self.y-4))
    
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
        x_move_to = x
        y_move_to = y
        x_shift = x_move_to - self.x
        y_shift = y_move_to - self.y
        if self.align == "Right":
            x_move_to = x - self.w
            x_shift = x_move_to - self.x + self.w
        self.textbox.move_to(x_move_to+10, y_move_to+9)
        self.rectangle_box.move_to(x_move_to, y_move_to)
        self.tail.move(x_shift, y_shift)
        self.x = x
        self.y = y

    def find_width(self):
        if self.text == "Jogging":
            self.w = 65
        elif self.text == "Homing":
            self.w = 60
        elif self.text == "Going to Pick":
            self.w = 95
        elif self.text == "Going to Place":
            self.w = 100
        elif self.text == "Going to Point":
            self.w = 100
        elif self.text == "Gripper Pick":
            self.w = 90
        elif self.text == "Gripper Place":
            self.w = 95
        elif self.text == "Please Connect the USB":
            self.w = 160
        elif self.text == "Protocol Error from Y-Axis":
            self.w = 170
        elif self.text == Error.code_1:
            self.w = 237
        elif self.text == Error.code_2:
            self.w = 275
        elif self.text == Error.code_3:
            self.w = 271
        elif self.text == Error.code_4x:
            self.w = 336
        elif self.text == Error.code_4y:
            self.w = 340
        else:
            self.w = int(len(self.text) * 7.5)


class Error:
    code_1  = "Input for Point Mode cannot be empty"
    code_2  = "Input for Point Mode cannot have 2 or more ."
    code_3  = "Input for Point Mode cannot have character"
    code_4x = "Input x for Point Mode must be between -15.0 and 15.0"
    code_4y = "Input y for Point Mode must be between -35.0 and 35.0"
