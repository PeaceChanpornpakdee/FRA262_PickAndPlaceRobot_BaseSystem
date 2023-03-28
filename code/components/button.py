from components.color import Color
from components.shape import Oval, Rectangle, RoundRectangle

class Button():
    """
    Button class
    """
    def create_click_area(self, shape, w, h):
        if shape == "rectangle":
            click_area = Rectangle(self.canvas, self.x, self.y, w, h, color="")
            return click_area.rectangle
        if shape == "oval":
            click_area = Oval(self.canvas, self.x, self.y, w, fill_color="", outline_color="")
            return click_area.oval


class ToggleButton(Button):
    """
    RadioButton class
    """
    def __init__(self, root_canvas, x, y, w, h, active_color, active_text, inactive_color, inactive_text, text_size, active_default):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.canvas = root_canvas.canvas
        self.active_color = active_color
        self.active_text  = active_text
        self.inactive_color = inactive_color
        self.inactive_text  = inactive_text
        self.text_size = text_size
        self.active = active_default
        self.create()

    def create(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        if self.active == True:
            self.round_rec = RoundRectangle(self.canvas, x, y, w, h, h/2, self.active_color)
            self.oval      = Oval(self.canvas, x+w-h+3, y+3, h-6, fill_color=Color.white, outline_color="")
        elif self.active == False:
            self.round_rec = RoundRectangle(self.canvas, x, y, w, h, h/2, self.inactive_color)
            self.oval      = Oval(self.canvas, x+3, y+3, h-6, fill_color=Color.white, outline_color="")
        self.click_area = self.create_click_area("rectangle", w, h)
        self.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", self.switch)

    def delete(self):
        self.round_rec.delete()
        self.oval.delete()

    def switch(self, event):
        self.active = not self.active
        self.delete()
        self.create()


class RadioButton(Button):
    """
    RadioButton class
    """
    def __init__(self, root_canvas, x, y, r, active_color, active_text, inactive_color, inactive_text, text_size, active_default):
        self.x = x
        self.y = y
        self.r = r
        self.canvas = root_canvas.canvas
        self.active_color = active_color
        self.active_text  = active_text
        self.inactive_color = inactive_color
        self.inactive_text  = inactive_text
        self.text_size = text_size
        self.active = active_default
        self.create()

    def create(self):
        x, y, r = self.x, self.y, self.r
        if self.active == True:
            self.outer_oval = Oval(self.canvas, x, y, r, fill_color="", outline_color=self.active_color)
            self.inner_oval = Oval(self.canvas, x+4, y+4, r-8, fill_color=self.active_color, outline_color="")
        elif self.active == False:
            self.outer_oval = Oval(self.canvas, x, y, r, fill_color="", outline_color=self.inactive_color)
        self.click_area = self.create_click_area("oval", r, r)
        self.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", self.clicked)

    def delete(self):
        self.outer_oval.delete()
        if not self.active:
            self.inner_oval.delete()

    def switch(self):
        self.active = not self.active
        self.delete()
        self.create()

    def clicked(self, event):
        if not self.active:
            self.switch()
