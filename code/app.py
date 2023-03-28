import pyglet
import tkinter as tk

from components.color import Color
from components.grid import Grid
from components.tray import Tray
from components.target import Target
from components.navigator import Navigator
from components.button import PressButton, RadioButton, ToggleButton
from components.shape import RoundRectangle
from components.textbox import TextBox
from components.photo import Photo

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

        self.field_canvas = tk.Canvas(self, width=840, height=540, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.field_canvas.pack(pady=30)
        self.field_background = RoundRectangle(self.field_canvas, 0, 0, 840, 540, 20, Color.whitegray)
        self.title_background = RoundRectangle(self.field_canvas, 600, 26, 240+20, 80, 20, Color.darkgray)
        TextBox(self.field_canvas, 690, 52, "Module III",  26, Color.lightblue)
        TextBox(self.field_canvas, 690, 82, "Base System", 19, Color.whitegray)
        Photo(self.field_canvas, "logo", 800, 66)

        self.grid = Grid(self.field_canvas, 20, 120, 70, 30, Color.lightgray)
        self.pick_tray = Tray(self.field_canvas, self.grid) 
        self.target =  Target(self.field_canvas, self.grid, grid_x=10, grid_y=10)
        self.navi = Navigator(self.field_canvas, self.grid, grid_x=-5, grid_y=10, grid_z=8)

        self.command_canvas = tk.Canvas(self, width=840, height=150, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.command_canvas.pack(pady=0)
        self.command_background = RoundRectangle(self.command_canvas, 0, 0, 840, 150, 20, Color.whitegray)
        
        TextBox(self.command_canvas, 75, 25, "End Effector", 16, Color.darkgray)
        TextBox(self.command_canvas, 75, 55, "Laser", 13, Color.darkgray)
        TextBox(self.command_canvas, 75, 75, "Gripper", 13, Color.darkgray)

        TextBox(self.command_canvas, 400, 25, "Operation", 16, Color.darkgray)
        TextBox(self.command_canvas, 700, 25, "Movement", 16, Color.darkgray)
        

        self.toggle = ToggleButton(canvas=self.command_canvas, x=100, y=100, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=True)
        
        self.operation_mode = "Tray"
        self.radio_1 = RadioButton(canvas=self.command_canvas, x=400, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Tray Mode",  text_size=12, active_default=True)
        self.radio_2 = RadioButton(canvas=self.command_canvas, x=500, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode", text_size=12, active_default=False)
        self.press_pick  = PressButton(canvas=self.command_canvas, x=400, y=80, w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Pick Tray", text_size=12, active_default=True)
        self.press_place = PressButton(canvas=self.command_canvas, x=400, y=110, w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Place Tray", text_size=12, active_default=True)

        self.press_home = PressButton(canvas=self.command_canvas, x=680, y=50, w=128, h=30, r=15, active_color=Color.gray, inactive_color=Color.lightgray, text="Home", text_size=15, active_default=True)
        self.press_run  = PressButton(canvas=self.command_canvas, x=680, y=90, w=128, h=44, r=22, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", text_size=22, active_default=True)


        self.command_canvas.create_line((280, 20), (280, 140), width=2, fill=Color.lightgray)
        self.command_canvas.create_line((620, 20), (620, 140), width=2, fill=Color.lightgray)

        if self.mode == "Developer":
            keyboard = Keyboard(self)
            keyboard.key_bind(self)

        # app.bind("<ButtonRelease-1>", mouse_position)
        # app.bind("<Motion>", mouse_position)
        # field_canvas.canvas.bind("<Motion>", mouse_position)
        self.field_canvas.bind("<ButtonRelease-1>", mouse_position)


    def task(self):

        if self.operation_mode == "Tray" and self.radio_2.active:
            self.radio_1.switch()
            self.operation_mode = "Point"

        elif self.operation_mode == "Point" and self.radio_1.active:
            self.radio_2.switch()
            self.operation_mode = "Tray"

        if self.press_run.pressed:
            print("Run")
            self.press_run.pressed = False

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