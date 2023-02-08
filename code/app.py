import pyglet
import tkinter as tk

from canvas import Canvas, ToggleButton, Navigator, Tray
from color import Color
from function import *
from keyboard import Keyboard

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Base System')

        #Mode
        self.mode = "Developer"

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

        self.grid_position = (0, 0)

    def task(self):
        #Get navi position then redraw
        self.navi.clear_navigator()
        self.navi.create_navigator()
        self.pick_tray.clear_tray()
        self.pick_tray.create_tray()

        self.after(10, self.task) 

if __name__ == "__main__":
    app = App()
    field_canvas   = Canvas(app, 840, 540, 30)
    command_canvas = Canvas(app, 840, 150, 0)

    field_canvas.create_round_rectangle(600, 26, 240+20, 80, 20, Color.darkgray)
    field_canvas.create_grid(20, 120, 70, 30, Color.lightgray)
    field_canvas.create_textbox(690, 52, "Module III", 26, Color.lightblue)
    field_canvas.create_textbox(690, 82, "Base System", 19, Color.whitegray)
    field_canvas.create_photo("logo", 800, 66)

    # field_canvas.create_tray(9, 30, 20)
    app.pick_tray = Tray(root_canvas=field_canvas) 

    # field_canvas.create_navigator(-10, 10, 8)
    app.navi = Navigator(root_canvas=field_canvas, grid_x=-5, grid_y=10, grid_z=8)

    # field_canvas.create_oval_point(-10, 10, 0)
    field_canvas.create_target_point(10, 10)
    # command_canvas.create_rectangle_button(0, 0, 100, 50, 20, Color.blue, "Run", 20, Color.white, hello)
    # command_canvas.create_radio_button(100, 100, 14, Color.blue, "active", hello)
    # command_canvas.create_radio_button(200, 100, 14, Color.blue, "inactive", hello)
    
    toggle = ToggleButton(root_canvas=command_canvas, x=300, y=100, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, function=laser_transmit)

    
    if app.mode == "Developer":
        keyboard = Keyboard(app)
        keyboard.key_bind(app)

    app.task()
    app.mainloop()