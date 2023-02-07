import pyglet
import tkinter as tk

from frame import Canvas
from color import Color

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Base System')

        # App window dimension
        window_width = 900
        window_height = 780

        # Find the center point
        center_x = int(self.winfo_screenwidth()/2 - window_width / 2)
        center_y = 0

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(bg=Color.darkgray)

        # Add font
        pyglet.font.add_file('font/Inter-Regular.ttf')

if __name__ == "__main__":
    app = App()
    field_canvas   = Canvas(app, 840, 540, 30)
    command_canvas = Canvas(app, 840, 150, 0)

    field_canvas.create_round_rectangle("TopLeft", 600, 25, 240+20, 80, 20, Color.darkgray)
    field_canvas.create_grid(20, 120, 70, 30, Color.lightgray)
    field_canvas.create_textbox(100, 200, "Hello", 25, Color.gray)

    app.mainloop()