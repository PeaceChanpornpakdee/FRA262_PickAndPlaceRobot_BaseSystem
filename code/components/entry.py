import tkinter as tk
from components.color import Color

class Entry():
    def __init__(self, master, canvas, x, y, color):
        self.master = master
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.string_var = tk.StringVar() 
        self.create()

    def create(self):
        self.entry = tk.Entry(master=self.master, bg=Color.whitegray, bd=2, font="Inter-SemiBold", fg=self.color, selectforeground=self.color, highlightthickness=0, insertbackground=self.color, insertwidth=2, justify="center", width=8, textvariable=self.string_var) 
        self.canvas.create_window(400, 100, window=self.entry)

    # def delete(self):
    #     self.entry.destroy()
    def error(self):
        self.entry.config({ "fg": Color.red, "selectforeground": Color.red, "insertbackground": Color.red })

    def normal(self):
        self.entry.config({ "fg": self.color, "selectforeground": self.color, "insertbackground": self.color })

    def get_value(self):
        return self.entry.get()

    def validate(self, value):
        valid_character = "1234567890."
        
        #Check if have 2 or more .
        if len(value.split(".")) > 2:
            print(False)
            return False
        
        #Check if only have numbers and .
        for character in str(value):
            print(character)
            if character not in valid_character:
                print(False)
                return False
        print(True)
        return True