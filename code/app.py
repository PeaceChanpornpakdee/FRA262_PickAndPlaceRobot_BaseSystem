import pyglet
import tkinter as tk

from canvas import Canvas
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
        pyglet.font.add_file('font/Inter-Bold.ttf')
        pyglet.font.add_file('font/Inter-SemiBold.ttf')

if __name__ == "__main__":
    app = App()
    field_canvas   = Canvas(app, 840, 540, 30)
    command_canvas = Canvas(app, 840, 150, 0)

    field_canvas.create_round_rectangle("TopLeft", 600, 26, 240+20, 80, 20, Color.darkgray)
    field_canvas.create_grid(20, 120, 70, 30, Color.lightgray)
    field_canvas.create_textbox(690, 52, "Module III", 26, Color.lightblue)
    field_canvas.create_textbox(690, 82, "Base System", 19, Color.whitegray)
    field_canvas.create_photo("logo", 800, 66)
    field_canvas.create_tray(9, 30, 20)
    field_canvas.create_navigator(-10, 10, 8)
    field_canvas.create_oval_point(-10, 10, 0)
    # field_canvas.create_target_point(10.2, 19.7)
    field_canvas.create_target_point(10, 10)

    app.mainloop()