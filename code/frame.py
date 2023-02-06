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
    def __init__(self, container, style):
        super().__init__(container)

        self.style = style
        # super().__init__(container)

    
        #canvas
        self.canvas = tk.Canvas(self, width=840, height=540, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge', cursor='dot')
        self.canvas.pack(anchor=tk.CENTER, expand=True, pady=30)
        self.round_rectangle(self.canvas, "TopLeft", 0, 0, 840, 540, 20, Color.white)
        self.round_rectangle(self.canvas, "TopLeft", 600, 25, 240+20, 80, 20, Color.darkgray)

        self.pack(padx=0, pady=0)

    def round_rectangle(self, canvas, mode, x, y, w, h, r, color):
        if mode == "Center":
            x = x - w/2
            y = y - h/2
        
        canvas.create_oval(x,       y,       x+2*r, y+2*r, fill=color, outline='')
        canvas.create_oval(x+w-2*r, y,       x+w,   y+2*r, fill=color, outline='')
        canvas.create_oval(x,       y+h-2*r, x+2*r, y+h,   fill=color, outline='')
        canvas.create_oval(x+w-2*r, y+h-2*r, x+w,   y+h,   fill=color, outline='')
        canvas.create_rectangle(x+r, y,   x+w-r, y+h,   fill=color, outline='')
        canvas.create_rectangle(x,   y+r, x+w,   y+h-r, fill=color, outline='')


# class TestFrame():
#     def __init__(self, container):
#         frame = ttk.Frame(container)
#         frame.pack(padx=10, pady=10)

def TestCanvas(container):
    canvas = tk.Canvas(container, width=840, height=540, bg=Color.gray, bd=0, highlightthickness=0, relief='ridge', cursor='dot')
    canvas.pack(pady=30)

    return canvas




class Canvas():
    def __init__(self, container):
        self.canvas = tk.Canvas(container, width=840, height=540, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge', cursor='dot')
        self.canvas.pack(pady=30)
        self.round_rectangle("TopLeft", 0, 0, 840, 540, 20, Color.white)
        self.round_rectangle("TopLeft", 600, 25, 240+20, 80, 20, Color.darkgray)

    def round_rectangle(self, mode, x, y, w, h, r, color):
        if mode == "Center":
            x = x - w/2
            y = y - h/2
        
        self.canvas.create_oval(x,       y,       x+2*r, y+2*r, fill=color, outline='')
        self.canvas.create_oval(x+w-2*r, y,       x+w,   y+2*r, fill=color, outline='')
        self.canvas.create_oval(x,       y+h-2*r, x+2*r, y+h,   fill=color, outline='')
        self.canvas.create_oval(x+w-2*r, y+h-2*r, x+w,   y+h,   fill=color, outline='')
        self.canvas.create_rectangle(x+r, y,   x+w-r, y+h,   fill=color, outline='')
        self.canvas.create_rectangle(x,   y+r, x+w,   y+h-r, fill=color, outline='')