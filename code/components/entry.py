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
        self.entry_window = self.canvas.create_window(self.x+59, self.y+11, window=self.entry)
        self.set_text("0.0")

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

    def set_text(self, text):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(text))

    def get_value(self):
        return self.entry.get()

    def validate(self, value, limit):
        """
        Parameters
            value (str) : Entry's value 
            limit (int) : Limit of entry's value
        
        Return
            Error code (int) : Error code where
                0 = Normal
                1 = Error Empty value
                2 = Error 2 or more .
                3 = Error have unsupported character
                4 = Error over limit
        """
        valid_character = "1234567890."

        value = str(value)

        # Remove blank space
        value = value.replace(" ", "")

        #Check if is an empty string
        if len(value) == 0:
            return 1
        
        #Check if have just -
        if value == "-" or value == ".":
            return 1

        #Check if have 2 or more .
        if len(value.split(".")) > 2:
            return 2
        
        #Check if only have numbers and . (and - at the beginning)
        for i in range(len(value)):
            if value[i] not in valid_character:
                if i != 0 or value[i] != "-":
                    return 3
                
        #Check if value is over limit
        if float(value) > limit:
            return 4
        if float(value) < -limit:
            return 4

        return 0