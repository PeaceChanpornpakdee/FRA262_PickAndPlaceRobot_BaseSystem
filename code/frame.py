import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from color import Color

class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        # label
        self.label = ttk.Label(self, text='Hello, Tkinter!')
        self.label.pack(**options)

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.pack(**options)

        # show the frame on the container
        self.pack(**options)

    def button_clicked(self):
        showinfo(title='Information',
                 message='Hello, Tkinter!')

class FieldFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #canvas
        self.canvas = tk.Canvas(self, width=840, height=540, bg=Color.gray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.canvas.create_oval(0,0,20,20, fill=Color.white, outline="")
        self.canvas.create_oval(820,0,840,20, fill=Color.white, outline="")
        self.canvas.create_oval(0,520,20,540, fill=Color.white, outline="")
        self.canvas.create_oval(820,520,840,540, fill=Color.white, outline="")

        options = {'padx': 0, 'pady': 0}
        # self.pack(**options)
        self.pack()