import pyglet
import tkinter as tk

from components.color import Color
from components.grid import Grid
from components.tray import Tray
from components.target import Target
from components.navigator import Navigator
from components.button import PressButton, RadioButton, ToggleButton
from components.shape import RoundRectangle, Line
from components.text import TextBox, MessageBox, Error
from components.photo import Photo
from components.entry import Entry

from keyboard import Keyboard
from protocol import Protocol

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Title
        self.title('Base System')
        # Mode
        self.mode = "Developer"
        # Window Dimension
        window_width = 900
        window_height = 780
        # Find Window Center
        window_center_x = int(self.winfo_screenwidth()/2 - window_width / 2)
        window_center_y = 0
        # Set Window Properties
        self.geometry(f'{window_width}x{window_height}+{window_center_x}+{window_center_y}')
        self.resizable(False, False)
        self.configure(bg=Color.darkgray)
        # Add Font
        pyglet.font.add_file('font/Inter-Bold.ttf')
        pyglet.font.add_file('font/Inter-SemiBold.ttf')
        # Create Components
        self.create_components()
        # Counting Time
        self.time_ms = 0
        # Prepare Protocol
        self.protocol = Protocol(self)
        self.connection = True
        self.new_connection = True

    def task(self):
        # Handle Buttons
        self.handle_toggle_laser()
        self.handle_toggle_gripper()
        self.handle_press_arrow()
        self.handle_radio_operation()
        self.handle_press_tray_pick()
        self.handle_press_tray_place()
        self.handle_press_home()
        self.handle_press_run()
        # Validate Entry Value
        self.validate_entry()
        # Perform Protocol Every 1 s
        if self.time_ms >= 1000:
            self.time_ms = 0
            # self.connection = self.protocol.heartbeat()
            self.new_connection = self.protocol.heartbeat()
            # self.protocol.routine()

        # If Connection is Changed 
        if self.connection != self.new_connection:
            # Update Connection Value
            self.connection = self.new_connection
            if not self.connection: # If Disconnected
                self.handle_disconnected()
            else: # If Reconnected
                self.handle_connected()

        # if self.homing or self.running:
        #     self.navi.move_to(10, 10)

        # Loop every 10 ms
        self.after(10, self.task) 
        self.time_ms += 10

    def create_components(self):
        # Field Canvas (Upper)
        self.canvas_field = tk.Canvas(master=self, width=840, height=540, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_field.pack(pady=30)
        self.background_field = RoundRectangle(canvas=self.canvas_field, x=0, y=0, w=840, h=540, r=20, color=Color.whitegray)
        # Title and Logo
        self.background_title = RoundRectangle(canvas=self.canvas_field, x=600, y=26, w=240+20, h=80, r=20, color=Color.darkgray)
        self.text_title = TextBox(canvas=self.canvas_field, x=690, y=52, text="Module III",  size=26, color=Color.lightblue)
        self.text_subtitle = TextBox(canvas=self.canvas_field, x=690, y=82, text="Base System", size=19, color=Color.whitegray)
        self.photo_logo = Photo(canvas=self.canvas_field, file_name="logo", x=800, y=66)
        # Grid
        self.grid = Grid(canvas=self.canvas_field, offset_x=20, offset_y=120, row=70, column=30, color=Color.lightgray)
        self.text_negative_x = TextBox(canvas=self.canvas_field, x=288, y=389, text="-x", size=15, color=Color.lightgray)
        self.text_positive_x = TextBox(canvas=self.canvas_field, x=553, y=251, text="+x", size=15, color=Color.lightgray)
        self.text_negative_y = TextBox(canvas=self.canvas_field, x=713, y=467, text="-y", size=15, color=Color.lightgray)
        self.text_positive_y = TextBox(canvas=self.canvas_field, x=127, y=170, text="+y", size=15, color=Color.lightgray)
        # Tray
        self.tray_pick = Tray(canvas=self.canvas_field, grid=self.grid, origin_x=-15, origin_y=30, orientation=0, navi=None) 
        self.tray_place = Tray(canvas=self.canvas_field, grid=self.grid, origin_x=9, origin_y=-35, orientation=0, navi=None) 
        self.show_tray_pick  = False
        self.show_tray_place = False
        # Target
        self.target =  Target(canvas=self.canvas_field, grid=self.grid, grid_x=0, grid_y=0)
        self.target.hide()
        self.point_target_x = 0
        self.point_target_y = 0
        # Navigator
        self.navi = Navigator(canvas=self.canvas_field, grid=self.grid, grid_x=0, grid_y=0, grid_z=8, pick_tray=self.tray_pick, place_tray=self.tray_place)
        self.tray_pick.navi = self.navi
        self.message_navi  = MessageBox(canvas=self.canvas_field, x=434, y=246,    text="Going Home", color=Color.blue, direction="NW", align="Left", size=11)
        self.message_laser = MessageBox(canvas=self.canvas_field, x=434, y=246+48, text="Gripper Pick", color=Color.blue, direction="SW", align="Left", size=11)
        self.message_laser.hide()
        # Status Text
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
        # Error Message Box
        self.message_error = MessageBox(canvas=self.canvas_field, x=810, y=490, text="Input x for Point Mode must be between -15.0 and 15.0", color=Color.red, direction="SE", align="Right", size=12)
        self.message_error.hide()
        # Connection Message Box
        self.message_connection = MessageBox(canvas=self.canvas_field, x=334, y=45, text="Connection Disconnected", color=Color.red, direction="C", align="Right", size=12)
        self.message_connection.hide()

        # Command Canvas (Lower)
        self.canvas_command = tk.Canvas(master=self, width=840, height=150, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_command.pack(pady=0)
        self.background_command = RoundRectangle(canvas=self.canvas_command, x=0, y=0, w=840, h=150, r=20, color=Color.whitegray)
        # End Effector Section
        self.text_end_eff   = TextBox(canvas=self.canvas_command, x=130, y=25,  text="End Effector", size=16, color=Color.darkgray)
        self.text_laser     = TextBox(canvas=self.canvas_command, x=90, y=62,  text="Laser", size=13, color=Color.darkgray)
        self.text_gripper   = TextBox(canvas=self.canvas_command, x=85, y=96, text="Gripper", size=13, color=Color.darkgray)
            # Toggle and Press Button
        self.toggle_laser   = ToggleButton(canvas=self.canvas_command, x=115, y=52, w=36, h=20, on_color=Color.blue, on_text="On", off_color=Color.lightgray, off_text="Off", text_size=12, on_default=False)
        self.toggle_gripper = ToggleButton(canvas=self.canvas_command, x=115, y=86, w=36, h=20, on_color=Color.blue, on_text="On", off_color=Color.lightgray, off_text="Off", text_size=12, on_default=False)
        self.direction_arrow = "pick"
        self.press_arrow    = PressButton(canvas=self.canvas_command, x=115, y=113, w=70, h=22, r=11, active_color=Color.gray, inactive_color=Color.lightgray, text="     Pick", text_size=12, active_default=False, image="arrow")
        # Operation Section
        self.text_opera  = TextBox(canvas=self.canvas_command, x=425, y=25, text="Operation", size=16, color=Color.darkgray)
        self.operation_mode = "Tray"
            # Mode Radio Button
        self.radio_tray  = RadioButton(canvas=self.canvas_command, x=330, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Tray Mode  ",  text_size=12, active_default=True)
        self.radio_point = RadioButton(canvas=self.canvas_command, x=440, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode",   text_size=12, active_default=False)
            # Set Tray Press Button
        self.press_pick  = PressButton(canvas=self.canvas_command, x=330, y=82,  w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Pick Tray", text_size=12, active_default=True)
        self.press_place = PressButton(canvas=self.canvas_command, x=330, y=112, w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Place Tray", text_size=12, active_default=True)
            # Entry Point
        self.entry_x = Entry(master=self, canvas=self.canvas_command, x=364, y=82,  color=Color.blue)
        self.entry_y = Entry(master=self, canvas=self.canvas_command, x=364, y=112, color=Color.blue)
        self.entry_normal = True
        self.entry_x_value = "0.0"
        self.entry_y_value = "0.0"
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
        # Movement Section
        self.text_movement = TextBox(self.canvas_command, 725, 25, "Movement", 16, Color.darkgray)
            # Home Press Button
        self.press_home = PressButton(canvas=self.canvas_command, x=655, y=50, w=128, h=30, r=15, active_color=Color.gray, inactive_color=Color.lightgray, text="Home", text_size=15, active_default=True)
        self.homing = False
            # Run Press Button
        self.press_run  = PressButton(canvas=self.canvas_command, x=655, y=90, w=128, h=44, r=22, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", text_size=22, active_default=True)
        self.running = False
        # Section Seperator
        self.line_separate_1 = Line(canvas=self.canvas_command, point_1=(260, 20), point_2=(260, 140), width=2, color=Color.lightgray)
        self.line_separate_2 = Line(canvas=self.canvas_command, point_1=(595, 20), point_2=(595, 140), width=2, color=Color.lightgray)

        # Get Goal Point from Mouse Click in Point Mode 
        self.canvas_field.bind("<ButtonRelease-1>", self.mouse_position)

        # Get Out of Entry when Press Enter of Click Outside the Entry 
        self.bind("<Return>", self.out_entry)
        self.canvas_command.bind("<Button-1>", self.out_entry)

        # Keyboard Control Navigator for Developer
        if self.mode == "Developer":
            keyboard = Keyboard(self)
            keyboard.key_bind(self)
        
    def mouse_position(self, event):
        if self.operation_mode == "Point" and self.connection:
            # Convert Pixel to Grid
            grid_x, grid_y = self.grid.map_2D_to_3D(event.x, event.y)
            # Reduce to 1 decimal point
            self.point_target_x = round(float(grid_x)+0.0000001, 1)
            self.point_target_y = round(float(grid_y)+0.0000001, 1)
            # Move Target to Desired Grid Position
            self.target.move_to(self.point_target_x, self.point_target_y)
            # Set Text in Entry
            self.entry_x.set_text(self.point_target_x)
            self.entry_y.set_text(self.point_target_y)

    def out_entry(self, event):
        if self.operation_mode == "Point":
            self.focus()
            # Move Target according to Entry's value if value is normal 
            if self.validate_entry() == "Normal":
                # Convert String (Entry's value) to Float and Reduce to 1 decimal point
                self.point_target_x = round(float(self.entry_x_value)+0.0000001, 1)
                self.point_target_y = round(float(self.entry_y_value)+0.0000001, 1)
                # Set Entry Text
                self.entry_x.set_text(str(self.point_target_x))
                self.entry_y.set_text(str(self.point_target_y))
                # Move Target
                self.target.move_to(self.point_target_x, self.point_target_y)

    def validate_entry(self):
        if self.operation_mode == "Point":
            # Get value from Entry
            self.entry_x_value = self.entry_x.get_value()
            self.entry_y_value = self.entry_y.get_value()
            # Validate Entry's Value
            validate_x_result = self.entry_x.validate(self.entry_x_value, 15)
            validate_y_result = self.entry_y.validate(self.entry_y_value, 35)
            # Interpret Validation Result
            validate_result = "Normal"
            if validate_y_result != 0:
                self.entry_y.error() # Entry Error (Red Text)
                validate_result = self.interpret_validate(validate_y_result, "y")
            else:
                self.entry_y.normal()
            if validate_x_result != 0:
                self.entry_x.error() # Entry Error (Red Text)
                validate_result = self.interpret_validate(validate_x_result, "x")
            else:
                self.entry_x.normal() # Entry Normal (Blue Text)
            # Display Error Message if Entry Error
            if validate_result != "Normal":
                self.message_error.change_text(validate_result)
                self.message_error.show()
            else:
                self.message_error.hide()
            # Return Validation Result
            return validate_result

        else:
            self.message_error.hide()
    
    def interpret_validate(self, validate_result, entry):
        # Convert Number Code from Validation Result to Error Text
        if validate_result == 1:
            return Error.code_1
        if validate_result == 2:
            return Error.code_2
        if validate_result == 3:
            return Error.code_3        
        if validate_result == 4:
            if entry == "x":
                return Error.code_4x
            if entry == "y":
                return Error.code_4y

    def turn_on_laser(self):
        print("Protocol - Laser On")
        self.toggle_laser.turn_on()
        self.navi.navigator_laser.show()
    
    def turn_off_laser(self):
        print("Protocol - Laser Off")
        self.toggle_laser.turn_off()
        self.navi.navigator_laser.hide()

    def turn_on_gripper(self):
        print("Protocol - Gripper On")
        self.toggle_gripper.turn_on()
        self.message_laser.show()

    def turn_off_gripper(self):
        print("Protocol - Gripper Off")
        self.toggle_gripper.turn_off()
        self.message_laser.hide()

    def handle_toggle_laser(self):
        if self.toggle_laser.pressed:
            print("handle_toggle_laser")
            # Turn Laser On
            if not self.toggle_laser.on:
                # Turn Gripper Off First
                if self.toggle_gripper.on:
                    self.turn_off_gripper()
                self.turn_on_laser()
            # Turn Laser Off
            else:
                self.turn_off_laser()
            self.toggle_laser.pressed = False

    def handle_toggle_gripper(self):
        if self.toggle_gripper.pressed:
            print("handle_toggle_gripper")
            # Turn Gripper On
            if not self.toggle_gripper.on:
                # Turn Laser Off First
                if self.toggle_laser.on:
                    self.turn_off_laser()
                self.turn_on_gripper()
            # Turn Gripper Off
            else:
                self.turn_off_gripper()
            self.toggle_gripper.pressed = False

        if self.connection:
            if self.toggle_gripper.on == False:
                self.press_arrow.deactivate()
            else:
                self.press_arrow.activate()

    def handle_press_arrow(self):
        if self.press_arrow.pressed:
            if self.toggle_gripper.on: 
                if self.direction_arrow == "pick":
                    print("Protocol - Gripper Pick")
                    self.press_arrow.photo_arrow_pick.hide()
                    self.press_arrow.photo_arrow_place.show()
                    self.direction_arrow = "place"
                    self.press_arrow.change_text("     Place")
                    self.message_laser.change_text("Gripper Pick")
                elif self.direction_arrow == "place":
                    print("Protocol - Gripper Place")
                    self.press_arrow.photo_arrow_place.hide()
                    self.press_arrow.photo_arrow_pick.show()
                    self.direction_arrow = "pick"
                    self.press_arrow.change_text("     Pick")
                    self.message_laser.change_text("Gripper Place")
                self.message_laser.show()
            self.press_arrow.pressed = False

    def handle_radio_operation(self):
        # Click Point Mode
        if self.operation_mode == "Tray" and self.radio_point.active:
            self.radio_tray.deactivate()
            self.operation_mode = "Point"
            self.press_pick.hide()
            self.press_place.hide()
            self.entry_x.show()
            self.entry_y.show()
            self.text_x_entry.show()
            self.text_y_entry.show()
            self.text_mm_x_entry.show()
            self.text_mm_y_entry.show()
            self.tray_pick.clear_tray()
            self.tray_place.clear_tray()
            self.target.show()
        # Click Tray Mode
        elif self.operation_mode == "Point" and self.radio_tray.active:
            self.radio_point.deactivate()
            self.operation_mode = "Tray"
            self.press_pick.show()
            self.press_place.show()
            self.entry_x.hide()
            self.entry_y.hide()
            self.text_x_entry.hide()
            self.text_y_entry.hide()
            self.text_mm_x_entry.hide()
            self.text_mm_y_entry.hide()
            self.target.hide()
            if self.show_tray_pick:
                self.tray_pick.create_tray()
            if self.show_tray_place:
                self.tray_place.create_tray()

    def handle_press_tray_pick(self):
        if self.press_pick.pressed:
            # Close Gripper & Open Laser First
            if not self.toggle_laser.on:
                self.toggle_laser.pressed = True
                self.handle_toggle_laser()
            print("Protocol - Set Pick Tray")
            self.tray_pick.clear_tray()
            # Wait for Origin & Orientation
            self.tray_pick.create_tray()
            self.show_tray_pick = True
            self.press_pick.pressed = False

    def handle_press_tray_place(self):
        if self.press_place.pressed:
            # Close Gripper & Open Laser First
            if not self.toggle_laser.on:
                self.toggle_laser.pressed = True
                self.handle_toggle_laser()
            print("Protocol - Set Place Tray")
            self.tray_place.clear_tray()
            # Wait for Origin & Orientation
            self.tray_place.create_tray()
            self.show_tray_place = True
            self.press_place.pressed = False

    def handle_press_home(self):
        if self.press_home.pressed:
            print("Protocol - Home")
            self.homing = True
            self.press_home.pressed = False

    def handle_press_run(self):
        if self.press_run.pressed:
            if self.operation_mode == "Tray":
                print("Protocol - Run Tray")
            elif self.operation_mode == "Point":
                print("Protocol - Set Goal Point")
                print("Protocol - Run Point")
            self.running = True
            if self.toggle_laser.on:
                self.turn_off_laser()
            if self.toggle_gripper.on:
                self.turn_off_gripper()
            self.toggle_laser.deactivate()
            self.toggle_gripper.deactivate()
            self.press_arrow.deactivate()
            self.press_pick.deactivate()
            self.press_place.deactivate()
            self.entry_x.disable()
            self.entry_y.disable()
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_run.pressed = False

    def handle_disconnected(self):
        self.message_connection.show()
        self.toggle_laser.deactivate()
        self.toggle_gripper.deactivate()
        self.press_arrow.deactivate()
        self.press_pick.deactivate()
        self.press_place.deactivate()
        self.entry_x.disable()
        self.entry_y.disable()
        self.press_run.deactivate()
        self.press_home.deactivate()
        self.text_x_pos_num.deactivate(self.text_x_pos_num.text, Color.lightgray)
        self.text_y_pos_num.deactivate(self.text_y_pos_num.text, Color.lightgray)
        self.text_y_spd_num.deactivate(self.text_y_spd_num.text, Color.lightgray)
        self.text_y_acc_num.deactivate(self.text_y_acc_num.text, Color.lightgray)
        
    def handle_connected(self):
        self.message_connection.hide()
        self.toggle_laser.activate()
        self.toggle_gripper.activate()
        self.press_arrow.activate()
        self.press_pick.activate()
        self.press_place.activate()
        self.entry_x.enable()
        self.entry_y.enable()
        self.press_run.activate()
        self.press_home.activate()
        self.text_x_pos_num.activate(self.text_x_pos_num.text, Color.blue)
        self.text_y_pos_num.activate(self.text_y_pos_num.text, Color.blue)
        self.text_y_spd_num.activate(self.text_y_spd_num.text, Color.blue)
        self.text_y_acc_num.activate(self.text_y_acc_num.text, Color.blue)


if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()