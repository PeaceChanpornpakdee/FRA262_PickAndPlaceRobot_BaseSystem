from components.color import Color

class Button():
    """
    Button class
    """
    def create_click_area(self, x, y, w, h, shape):
        if shape == "rectangle":
            return self.root_canvas.canvas.create_rectangle(x, y, x+w, y+h, fill="", outline="")
        if shape == "oval":
            return self.root_canvas.canvas.create_oval(x, y, x+w, y+h, fill="", outline="")

class ToggleButton(Button):
    """
    ToggleButton class
    """
    def __init__(self, root_canvas, x, y, w, h, active_color, active_text, inactive_color, inactive_text, text_size, function):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.root_canvas = root_canvas
        self.active_color = active_color
        self.active_text  = active_text
        self.inactive_color = inactive_color
        self.inactive_text  = inactive_text
        self.text_size = text_size
        self.function = function
        self.status = "inactive"
        self.create_toggle_button()

    def clicked(self, event):
        if self.status == "inactive":
            self.status = "active"
        else:
            self.status = "inactive"
        self.function(self.status)
        # self.root_canvas.canvas.delete("all")
        self.create_toggle_button()

    def create_toggle_button(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        if self.status == "active":
            self.root_canvas.create_round_rectangle(x, y, w, h, h/2, self.active_color)
            self.root_canvas.canvas.create_oval(x+w-h+3, y+3, x+w-3, y+h-3, fill=Color.white, outline="")
        elif self.status == "inactive":
            self.root_canvas.create_round_rectangle(x, y, w, h, h/2, self.inactive_color)
            self.root_canvas.canvas.create_oval(x+3, y+3, x+h-3, y+h-3, fill=Color.white, outline="")  
        self.click_area = self.create_click_area(x, y, w, h, "rectangle")
        self.root_canvas.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", self.clicked)