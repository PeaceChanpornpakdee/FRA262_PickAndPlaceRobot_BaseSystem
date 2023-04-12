from components.color import Color
from components.shape import Oval, Rectangle, RoundRectangle
from components.photo import Photo
from components.text import TextBox

class Button():
    """
    Button class
    """
    def create_click_area(self, w, h):
        return Rectangle(self.canvas, self.x, self.y, w, h, color="")
        

class PressButton(Button):
    """
    RectangleButton Class
    """
    def __init__(self, canvas, x, y, w, h, r, active_color, inactive_color, text, text_size, active_default, image=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text = text
        self.text_size = text_size
        self.active = active_default
        self.image = image
        self.pressed = False
        self.round_rec = RoundRectangle(self.canvas, x, y, w, h, r, color=self.active_color)
        self.textbox = TextBox(self.canvas, x+w/2, y+h/2, self.text, self.text_size, Color.white)
        if self.image != None:
            self.photo_arrow_pick  = Photo(canvas=canvas, file_name="arrow_pick",  x=130, y=124)
            self.photo_arrow_place = Photo(canvas=canvas, file_name="arrow_place", x=130, y=124)
            self.photo_arrow_place.hide()
        self.click_area = self.create_click_area(self.w, self.h)
        self.canvas.tag_bind(self.click_area.rect, "<ButtonRelease-1>", self.clicked)
        if self.active == False:
            self.deactivate()

    def hide(self):
        self.round_rec.hide()
        self.click_area.hide()

    def show(self):
        self.round_rec.show()
        self.click_area.show()

    def activate(self):
        self.active = True
        self.round_rec.activate(self.active_color)
    
    def deactivate(self):
        self.active = False
        self.round_rec.deactivate(self.inactive_color)

    def clicked(self, event):
        if self.active:
            self.pressed = True

    def change_text(self, text):
        self.textbox.change_text(text)


class RadioButton(Button):
    """
    RadioButton class
    """
    def __init__(self, canvas, x, y, r, active_color, inactive_color, text, text_size, active_default):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text = text
        self.text_size = text_size
        self.active = active_default
        self.outer_oval = Oval(self.canvas, x, y, r, fill_color="", outline_color=self.active_color)
        self.inner_oval = Oval(self.canvas, x+4, y+4, r-8, fill_color=self.active_color, outline_color="")
        self.textbox = TextBox(self.canvas, x+55, y+r/2, self.text, self.text_size, self.active_color)
        self.click_area = self.create_click_area(85, r)
        self.canvas.tag_bind(self.click_area.rect, "<ButtonRelease-1>", self.clicked)
        if self.active == False:
            self.deactivate()

    def activate(self):
        self.canvas.itemconfigure(self.outer_oval.oval, outline=self.active_color)
        self.inner_oval.show()
        self.textbox.activate(self.text, self.active_color)
    
    def deactivate(self):
        self.canvas.itemconfigure(self.outer_oval.oval, outline=self.inactive_color)
        self.inner_oval.hide()
        self.textbox.deactivate(self.text, self.inactive_color)

    def switch(self):
        self.active = not self.active
        if self.active:
            self.activate()
        else:
            self.deactivate()

    def clicked(self, event):
        if not self.active:
            self.switch()


class ToggleButton(Button):
    """
    ToggleButton class
    """
    def __init__(self, canvas, x, y, w, h, on_color, on_text, off_color, off_text, text_size, on_default):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.on_color = on_color
        self.on_text  = on_text
        self.off_color = off_color
        self.off_text  = off_text
        self.text_size = text_size
        self.on = on_default
        self.active = True
        self.pressed = False
        self.round_rec = RoundRectangle(self.canvas, x, y, w, h, h/2, self.on_color)
        self.oval      = Oval(self.canvas, x+w-h+3, y+3, h-6, fill_color=Color.white, outline_color="")
        self.textbox = TextBox(self.canvas, x+55, y+h/2, self.on_text, self.text_size, self.on_color)
        self.click_area = self.create_click_area(w, h)
        self.canvas.tag_bind(self.click_area.rect, "<ButtonRelease-1>", self.clicked)
        if not self.on:
            self.turn_off()

    def turn_on(self):
        self.round_rec.activate(self.on_color)
        self.canvas.move(self.oval.oval, self.w-self.h, 0)
        self.textbox.activate(self.on_text, self.on_color)
    
    def turn_off(self):
        self.round_rec.deactivate(self.off_color)
        self.canvas.move(self.oval.oval, self.h-self.w, 0)
        self.textbox.deactivate(self.off_text, self.off_color)

    def switch(self):
        self.on = not self.on
        if self.on:
            self.turn_on()
        else:
            self.turn_off()

    def clicked(self, event):
        if self.active:
            self.pressed = True

    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False