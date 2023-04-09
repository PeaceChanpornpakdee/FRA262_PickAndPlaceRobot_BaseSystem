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
from components.entry import Entry

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
        self.text_negative_x = TextBox(canvas=self.canvas_field, x=288, y=389, text="-x", size=15, color=Color.lightgray)
        self.text_positive_x = TextBox(canvas=self.canvas_field, x=553, y=251, text="+x", size=15, color=Color.lightgray)
        self.text_negative_y = TextBox(canvas=self.canvas_field, x=713, y=467, text="-y", size=15, color=Color.lightgray)
        self.text_positive_y = TextBox(canvas=self.canvas_field, x=127, y=170, text="+y", size=15, color=Color.lightgray)
        
        self.tray_pick = Tray(canvas=self.canvas_field, grid=self.grid) 
        self.target =  Target(canvas=self.canvas_field, grid=self.grid, grid_x=10, grid_y=10)
        self.navi = Navigator(canvas=self.canvas_field, grid=self.grid, grid_x=-5, grid_y=10, grid_z=8)

        self.text_x_pos = TextBox(canvas=self.canvas_field, x=82, y=418+5,  text="x-Axis Position", size=12, color=Color.darkgray)
        self.text_y_pos = TextBox(canvas=self.canvas_field, x=82, y=444+5,  text="y-Axis Position", size=12, color=Color.darkgray)
        self.text_y_spd = TextBox(canvas=self.canvas_field, x=77, y=470+5,  text="y-Axis Speed", size=12, color=Color.darkgray)
        self.text_y_acc = TextBox(canvas=self.canvas_field, x=95, y=496+5,  text="y-Axis Acceleration", size=12, color=Color.darkgray)

        self.text_x_pos_num = TextBox(canvas=self.canvas_field, x=185, y=418+5,  text="- 12.2", size=12, color=Color.blue)
        self.text_y_pos_num = TextBox(canvas=self.canvas_field, x=185, y=444+5,  text="26.4", size=12, color=Color.blue)
        self.text_y_spd_num = TextBox(canvas=self.canvas_field, x=185, y=470+5,  text="400.0", size=12, color=Color.blue)
        self.text_y_acc_num = TextBox(canvas=self.canvas_field, x=185, y=496+5,  text="300.0", size=12, color=Color.blue)

        self.text_x_pos_mm = TextBox(canvas=self.canvas_field, x=228, y=418+5,  text="mm", size=11, color=Color.darkgray)
        self.text_y_pos_mm = TextBox(canvas=self.canvas_field, x=228, y=444+5,  text="mm", size=11, color=Color.darkgray)
        self.text_y_spd_mm = TextBox(canvas=self.canvas_field, x=233, y=470+5,  text="mm/s", size=11, color=Color.darkgray)
        self.text_y_acc_mm = TextBox(canvas=self.canvas_field, x=233, y=496+5,  text="mm/s", size=11, color=Color.darkgray)
        self.text_y_acc_2  = TextBox(canvas=self.canvas_field, x=250, y=494+5,  text="2", size=8, color=Color.darkgray)

        # self.balloon_text = TextBox(canvas=self.canvas_field, x=200, y=100,  text="The maximum input is \n700 mm for width", size=11, color=Color.darkgray)        


        self.canvas_command = tk.Canvas(master=self, width=840, height=150, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_command.pack(pady=0)
        self.background_command = RoundRectangle(canvas=self.canvas_command, x=0, y=0, w=840, h=150, r=20, color=Color.whitegray)
        
        self.text_end_eff   = TextBox(canvas=self.canvas_command, x=130, y=25,  text="End Effector", size=16, color=Color.darkgray)
        self.text_laser     = TextBox(canvas=self.canvas_command, x=90, y=62,  text="Laser", size=13, color=Color.darkgray)
        self.text_gripper   = TextBox(canvas=self.canvas_command, x=85, y=96, text="Gripper", size=13, color=Color.darkgray)
        self.toggle_laser   = ToggleButton(canvas=self.canvas_command, x=115, y=52, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=False)
        self.toggle_gripper = ToggleButton(canvas=self.canvas_command, x=115, y=86, w=36, h=20, active_color=Color.blue, active_text="On", inactive_color=Color.lightgray, inactive_text="Off", text_size=12, active_default=False)
        self.direction_arrow = "pick"
        self.press_arrow    = PressButton(canvas=self.canvas_command, x=115, y=113, w=70, h=22, r=11, active_color=Color.gray, inactive_color=Color.lightgray, text="     Pick", text_size=12, active_default=False, image="arrow")

        self.text_opera  = TextBox(canvas=self.canvas_command, x=425, y=25, text="Operation", size=16, color=Color.darkgray)
        self.operation_mode = "Tray"
        self.radio_tray  = RadioButton(canvas=self.canvas_command, x=330, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Tray Mode  ",  text_size=12, active_default=True)
        self.radio_point = RadioButton(canvas=self.canvas_command, x=440, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode",   text_size=12, active_default=False)
        
        self.press_pick  = PressButton(canvas=self.canvas_command, x=330, y=82,  w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Pick Tray", text_size=12, active_default=True)
        self.press_place = PressButton(canvas=self.canvas_command, x=330, y=112, w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Place Tray", text_size=12, active_default=True)
        
        self.entry_x = Entry(master=self, canvas=self.canvas_command, x=364, y=82,  color=Color.blue)
        self.entry_y = Entry(master=self, canvas=self.canvas_command, x=364, y=112, color=Color.blue)
        self.text_x_entry = TextBox(canvas=self.canvas_command, x=345, y=90,  text="x", size=13, color=Color.darkgray)
        self.text_y_entry = TextBox(canvas=self.canvas_command, x=345, y=122,  text="y", size=13, color=Color.darkgray)
        self.text_mm_x_entry = TextBox(canvas=self.canvas_command, x=510, y=90,  text="mm", size=13, color=Color.darkgray)
        self.text_mm_y_entry = TextBox(canvas=self.canvas_command, x=510, y=122,  text="mm", size=13, color=Color.darkgray)
        self.entry_x.hide()
        self.entry_y.hide()
        self.text_x_entry.hide()
        self.text_y_entry.hide()
        self.text_mm_x_entry.hide()
        self.text_mm_y_entry.hide()
                
        self.text_movement = TextBox(self.canvas_command, 725, 25, "Movement", 16, Color.darkgray)
        self.press_home = PressButton(canvas=self.canvas_command, x=655, y=50, w=128, h=30, r=15, active_color=Color.gray, inactive_color=Color.lightgray, text="Home", text_size=15, active_default=True)
        self.press_run  = PressButton(canvas=self.canvas_command, x=655, y=90, w=128, h=44, r=22, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", text_size=22, active_default=True)


        self.canvas_command.create_line((260, 20), (260, 140), width=2, fill=Color.lightgray)
        self.canvas_command.create_line((595, 20), (595, 140), width=2, fill=Color.lightgray)

        if self.mode == "Developer":
            keyboard = Keyboard(self)
            keyboard.key_bind(self)

        # app.bind("<ButtonRelease-1>", mouse_position)
        # app.bind("<Motion>", mouse_position)
        # canvas_field.canvas.bind("<Motion>", mouse_position)
        self.canvas_field.bind("<ButtonRelease-1>", mouse_position)

        self.bind("<Return>", self.remove_focus)
        self.canvas_command.bind("<Button-1>", self.remove_focus)

    def remove_focus(self, event):
        self.focus()

    def task(self):

        if self.operation_mode == "Tray" and self.radio_point.active:
            self.radio_tray.switch()
            self.operation_mode = "Point"
            self.press_pick.hide()
            self.press_place.hide()
            self.entry_x.show()
            self.entry_y.show()
            self.text_x_entry.show()
            self.text_y_entry.show()
            self.text_mm_x_entry.show()
            self.text_mm_y_entry.show()

        elif self.operation_mode == "Point" and self.radio_tray.active:
            self.radio_point.switch()
            self.operation_mode = "Tray"
            self.press_pick.show()
            self.press_place.show()
            self.entry_x.hide()
            self.entry_y.hide()
            self.text_x_entry.hide()
            self.text_y_entry.hide()
            self.text_mm_x_entry.hide()
            self.text_mm_y_entry.hide()


        if self.toggle_laser.pressed:
            self.toggle_laser.switch()
            if self.toggle_laser.active:
                if self.toggle_gripper.active:
                    self.toggle_gripper.switch()
                    print("Protocol - Gripper Off")
                print("Protocol - Laser On")
            else:
                print("Protocol - Laser Off")
            self.toggle_laser.pressed = False

        if self.toggle_gripper.pressed:
            self.toggle_gripper.switch()
            if self.toggle_gripper.active:
                if self.toggle_laser.active:
                    self.toggle_laser.switch()
                    print("Protocol - Laser Off")
                print("Protocol - Gripper On")
            else:
                print("Protocol - Gripper Off")
            self.toggle_gripper.pressed = False

        if self.toggle_gripper.active == False:
            self.press_arrow.deactivate()
        else:
            self.press_arrow.activate()

        if self.press_arrow.pressed:
            if self.direction_arrow == "pick":
                print("Protocol - Gripper Pick")
                self.press_arrow.photo_arrow_pick.hide()
                self.press_arrow.photo_arrow_place.show()
                self.direction_arrow = "place"
                self.press_arrow.change_text("     Place")
            elif self.direction_arrow == "place":
                print("Protocol - Gripper Place")
                self.press_arrow.photo_arrow_place.hide()
                self.press_arrow.photo_arrow_pick.show()
                self.direction_arrow = "pick"
                self.press_arrow.change_text("     Pick")
            self.press_arrow.pressed = False

        if self.press_pick.pressed:
            print("Protocol - Set Pick Tray")
            self.press_pick.pressed = False

        if self.press_place.pressed:
            print("Protocol - Set Place Tray")
            self.press_place.pressed = False

        if self.press_home.pressed:
            print("Protocol - Home")
            self.press_home.pressed = False
        
        if self.press_run.pressed:
            print("Protocol - Run")
            self.entry_x.disable()
            self.entry_y.disable()
            self.press_run.deactivate()
            self.press_run.pressed = False

        #Remove in the Future
        self.tray_pick.clear_tray()
        self.tray_pick.create_tray()
        self.target.clear_target()
        self.target.create_target()
        self.navi.clear_navigator()
        self.navi.create_navigator()


        if not self.entry_x.validate(self.entry_x.get_value()):
            self.entry_x.error()
        else:
            self.entry_x.normal()

        if not self.entry_y.validate(self.entry_y.get_value()):
            self.entry_y.error()
        else:
            self.entry_y.normal()

        self.after(10, self.task) 

if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()