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

        self.canvas_field = tk.Canvas(master=self, width=840, height=540, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_field.pack(pady=30)
        self.background_field = RoundRectangle(canvas=self.canvas_field, x=0, y=0, w=840, h=540, r=20, color=Color.whitegray)
        self.background_title = RoundRectangle(canvas=self.canvas_field, x=600, y=26, w=240+20, h=80, r=20, color=Color.darkgray)
        self.text_title = TextBox(canvas=self.canvas_field, x=690, y=52, text="Module III",  size=26, color=Color.lightblue)
        self.text_subtitle = TextBox(canvas=self.canvas_field, x=690, y=82, text="Base System", size=19, color=Color.whitegray)
        self.photo_logo = Photo(canvas=self.canvas_field, file_name="logo", x=800, y=66)

        self.grid = Grid(canvas=self.canvas_field, offset_x=20, offset_y=120, row=70, column=30, color=Color.lightgray)
        self.tray_pick = Tray(canvas=self.canvas_field, grid=self.grid) 
        self.target =  Target(canvas=self.canvas_field, grid=self.grid, grid_x=10, grid_y=10)
        self.navi = Navigator(canvas=self.canvas_field, grid=self.grid, grid_x=-5, grid_y=10, grid_z=8)

        self.canvas_command = tk.Canvas(master=self, width=840, height=150, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_command.pack(pady=0)
        self.background_command = RoundRectangle(canvas=self.canvas_command, x=0, y=0, w=840, h=150, r=20, color=Color.whitegray)
        
        self.text_end_eff   = TextBox(canvas=self.canvas_command, x=75, y=25,  text="End Effector", size=16, color=Color.darkgray)
        self.text_laser     = TextBox(canvas=self.canvas_command, x=75, y=60,  text="Laser", size=13, color=Color.darkgray)
        self.text_gripper   = TextBox(canvas=self.canvas_command, x=75, y=100, text="Gripper", size=13, color=Color.darkgray)
        self.toggle_gripper = ToggleButton(canvas=self.canvas_command, x=100, y=90, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=True)
        self.toggle_laser   = ToggleButton(canvas=self.canvas_command, x=100, y=50, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=True)
        

        self.text_opera  = TextBox(canvas=self.canvas_command, x=400, y=25, text="Operation", size=16, color=Color.darkgray)
        self.operation_mode = "Tray"
        self.radio_tray  = RadioButton(canvas=self.canvas_command, x=400, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Tray Mode  ",  text_size=12, active_default=True)
        self.radio_point = RadioButton(canvas=self.canvas_command, x=500, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode",   text_size=12, active_default=False)
        self.press_pick  = PressButton(canvas=self.canvas_command, x=400, y=80,  w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Pick Tray", text_size=12, active_default=True)
        self.press_place = PressButton(canvas=self.canvas_command, x=400, y=110, w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Place Tray", text_size=12, active_default=True)

        
        self.text_movement = TextBox(self.canvas_command, 700, 25, "Movement", 16, Color.darkgray)
        self.press_home = PressButton(canvas=self.canvas_command, x=680, y=50, w=128, h=30, r=15, active_color=Color.gray, inactive_color=Color.lightgray, text="Home", text_size=15, active_default=True)
        self.press_run  = PressButton(canvas=self.canvas_command, x=680, y=90, w=128, h=44, r=22, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", text_size=22, active_default=True)


        self.canvas_command.create_line((280, 20), (280, 140), width=2, fill=Color.lightgray)
        self.canvas_command.create_line((620, 20), (620, 140), width=2, fill=Color.lightgray)

        if self.mode == "Developer":
            keyboard = Keyboard(self)
            keyboard.key_bind(self)

        # app.bind("<ButtonRelease-1>", mouse_position)
        # app.bind("<Motion>", mouse_position)
        # canvas_field.canvas.bind("<Motion>", mouse_position)
        self.canvas_field.bind("<ButtonRelease-1>", mouse_position)


    def task(self):

        if self.operation_mode == "Tray" and self.radio_point.active:
            self.radio_tray.switch()
            self.operation_mode = "Point"

        elif self.operation_mode == "Point" and self.radio_tray.active:
            self.radio_point.switch()
            self.operation_mode = "Tray"

        if self.press_run.pressed:
            print("Run")
            self.press_run.pressed = False

        #Remove in the Future
        self.tray_pick.clear_tray()
        self.tray_pick.create_tray()
        self.target.clear_target()
        self.target.create_target()
        self.navi.clear_navigator()
        self.navi.create_navigator()

        self.after(10, self.task) 

if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()