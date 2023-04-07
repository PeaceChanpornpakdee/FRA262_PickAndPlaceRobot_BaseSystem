import tkinter as tk
from components.color import Color
from components.shape import RoundRectangle

class Entry():
    def __init__(self, master, canvas, x, y, color):
        self.master = master
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.string_var = tk.StringVar() 
        self.outer_rec = RoundRectangle(canvas=self.canvas, x=self.x,   y=self.y,   w=120, h=24, r=12, color=Color.gray)
        self.inner_rec = RoundRectangle(canvas=self.canvas, x=self.x+2, y=self.y+2, w=116, h=20, r=10, color=Color.whitegray)
        self.entry = tk.Entry(master=self.master, bg=Color.whitegray, bd=0, font="Inter-SemiBold", fg=self.color, selectforeground=self.color, highlightthickness=0, insertbackground=self.color, insertwidth=2, justify="center", width=8, textvariable=self.string_var) 
        self.entry_window = self.canvas.create_window(self.x+54, self.y+11, window=self.entry)

    def hide(self):
        self.outer_rec.hide()
        self.inner_rec.hide()
        self.canvas.itemconfigure(self.entry_window, state='hidden')

    def show(self):
        self.outer_rec.show()
        self.inner_rec.show()
        self.canvas.itemconfigure(self.entry_window, state='normal')

    def error(self):
        self.entry.config({ "fg": Color.red, "selectforeground": Color.red, "insertbackground": Color.red })

    def normal(self):
        self.entry.config({ "fg": self.color, "selectforeground": self.color, "insertbackground": self.color })

    def disable(self):
        self.entry.config({ "state": "disabled" })
    
    def enable(self):
        self.entry.config({ "state": "normal" })

    def get_value(self):
        return self.entry.get()

    def validate(self, value):
        valid_character = "1234567890."
        #Check if have 2 or more .
        if len(value.split(".")) > 2:
            return False
        #Check if only have numbers and .
        for character in str(value):
            if character not in valid_character:
                return False
        return True