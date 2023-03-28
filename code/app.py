import pyglet
import tkinter as tk

from components.color import Color
from components.canvas import Canvas
from components.grid import Grid
from components.tray import Tray
from components.target import Target
from components.navigator import Navigator
from components.button import ToggleButton, RadioButton
from components.shape import RoundRectangle

from function import *
from keyboard import Keyboard

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #Title
        self.title('Base System')
        #Mode
        self.mode = "Developer"
        #Window Dimension
        window_width = 900
        window_height = 780
        #Find Center Point
        center_x = int(self.winfo_screenwidth()/2 - window_width / 2)
        center_y = 0
        #Set Window Properties
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(bg=Color.darkgray)
        #Add font
        pyglet.font.add_file('font/Inter-Bold.ttf')
        pyglet.font.add_file('font/Inter-SemiBold.ttf')
        #Components
        self.create_components()

    def create_components(self):
        self.field_canvas = Canvas(self, 840, 540, 30)
        self.field_background = RoundRectangle(self.field_canvas, 0, 0, 840, 540, 20, Color.whitegray)
        self.title_background = RoundRectangle(self.field_canvas, 600, 26, 240+20, 80, 20, Color.darkgray)
        # self.field_canvas.create_round_rectangle(600, 26, 240+20, 80, 20, Color.darkgray)
        self.field_canvas.create_textbox(690, 52, "Module III", 26, Color.lightblue)
        self.field_canvas.create_textbox(690, 82, "Base System", 19, Color.whitegray)
        self.field_canvas.create_photo("logo", 800, 66)

        self.grid = Grid(self.field_canvas, 20, 120, 70, 30, Color.lightgray)
        self.pick_tray = Tray(root_canvas=self.field_canvas, root_grid=self.grid) 
        self.target =  Target(root_canvas=self.field_canvas, root_grid=self.grid, grid_x=10, grid_y=10)
        self.navi = Navigator(root_canvas=self.field_canvas, root_grid=self.grid, grid_x=-5, grid_y=10, grid_z=8)
        
        self.command_canvas = Canvas(self, 840, 150, 0)
        self.command_background = RoundRectangle(self.command_canvas, 0, 0, 840, 150, 20, Color.whitegray)
        self.command_canvas.create_textbox(75, 25, "End Effector", 16, Color.darkgray)
        self.command_canvas.create_textbox(75, 55, "Laser", 13, Color.darkgray)
        self.command_canvas.create_textbox(75, 75, "Gripper", 13, Color.darkgray)

        self.command_canvas.create_textbox(400, 25, "Operation", 16, Color.darkgray)
        self.command_canvas.create_textbox(700, 25, "Movement", 16, Color.darkgray)
        # command_canvas.create_rectangle_button(0, 0, 100, 50, 20, Color.blue, "Run", 20, Color.white, hello)
        # command_canvas.create_radio_button(100, 100, 14, Color.blue, "active", hello)
        # command_canvas.create_radio_button(200, 100, 14, Color.blue, "inactive", hello)
        
        self.toggle = ToggleButton(root_canvas=self.command_canvas, x=300, y=100, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=True)
        
        self.operation_mode = "Tray"
        self.radio_1 = RadioButton(root_canvas=self.command_canvas, x=100, y=100, r=14, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=True)
        self.radio_2 = RadioButton(root_canvas=self.command_canvas, x=200, y=100, r=14, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=False)

        if self.mode == "Developer":
            keyboard = Keyboard(self)
            keyboard.key_bind(self)

        # app.bind("<ButtonRelease-1>", mouse_position)
        # app.bind("<Motion>", mouse_position)
        # field_canvas.canvas.bind("<Motion>", mouse_position)
        self.field_canvas.canvas.bind("<ButtonRelease-1>", mouse_position)


    def task(self):

        if self.operation_mode == "Tray" and self.radio_2.active:
            self.radio_1.switch()
            self.operation_mode = "Point"

        elif self.operation_mode == "Point" and self.radio_1.active:
            self.radio_2.switch()
            self.operation_mode = "Tray"

        #Remove in the Future
        self.pick_tray.clear_tray()
        self.pick_tray.create_tray()
        self.target.clear_target()
        self.target.create_target()
        self.navi.clear_navigator()
        self.navi.create_navigator()

        self.after(10, self.task) 

if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()