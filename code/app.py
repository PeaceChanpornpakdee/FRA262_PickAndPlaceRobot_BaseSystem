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
from protocol import Protocol_Y, Protocol_X

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
        self.protocol_y = Protocol_Y()
        self.protocol_x = Protocol_X()
        self.usb_connect = self.protocol_y.usb_connect
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

        # Handle y-axis protocol
        self.handle_protocol_y()

        # Handle x-axis protocol

        # Validate Entry Value
        self.validate_entry()

        # Loop every 10 ms
        self.after(10, self.task)
        self.time_ms += 10

    def create_components(self):
        """
        This function creates each UI components
        """
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
        self.tray_pick = Tray(canvas=self.canvas_field, grid=self.grid, origin_x=-15, origin_y=30, orientation=0) 
        self.tray_place = Tray(canvas=self.canvas_field, grid=self.grid, origin_x=9, origin_y=-35, orientation=0) 
        self.show_tray_pick  = False
        self.show_tray_place = False
        # Target
        self.target =  Target(canvas=self.canvas_field, grid=self.grid, grid_x=0, grid_y=0)
        self.target.hide()
        self.point_target_x = 0
        self.point_target_y = 0
        # Navigator
        self.navi = Navigator(canvas=self.canvas_field, grid=self.grid, grid_x=0, grid_y=0, grid_z=8, pick_tray=self.tray_pick, place_tray=self.tray_place)
        self.message_navi  = MessageBox(canvas=self.canvas_field, x=434, y=246,    text="Homing", color=Color.blue, direction="NW", align="Left", size=11)
        self.message_laser = MessageBox(canvas=self.canvas_field, x=434, y=246+48, text="Gripper Pick", color=Color.blue, direction="SW", align="Left", size=11)
        self.message_navi.hide()
        self.message_laser.hide()
        self.tray_pick.navi = self.navi
        self.tray_pick.message_navi = self.message_navi
        self.tray_pick.message_laser = self.message_laser
        self.tray_place.navi = self.navi
        self.tray_place.message_navi = self.message_navi
        self.tray_place.message_laser = self.message_laser
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
        self.message_connection = MessageBox(canvas=self.canvas_field, x=330, y=45, text="Connection Disconnected", color=Color.red, direction="C", align="Left", size=12)
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
        self.toggle_laser   = ToggleButton(canvas=self.canvas_command, x=115, y=52, w=36, h=20, on_color=Color.blue, on_text="On", off_color=Color.gray, off_text="Off", text_size=12, on_default=False)
        self.toggle_gripper = ToggleButton(canvas=self.canvas_command, x=115, y=86, w=36, h=20, on_color=Color.blue, on_text="On", off_color=Color.gray, off_text="Off", text_size=12, on_default=False)
        self.direction_arrow = "pick"
        self.press_arrow    = PressButton(canvas=self.canvas_command, x=115, y=113, w=70, h=22, r=11, active_color=Color.gray, inactive_color=Color.lightgray, text="     Pick", text_size=12, active_default=False, image="arrow")
        self.gripping = False
        # Operation Section
        self.text_opera  = TextBox(canvas=self.canvas_command, x=425, y=25, text="Operation", size=16, color=Color.darkgray)
        self.operation_mode = "Tray"
            # Mode Radio Button
        self.radio_tray  = RadioButton(canvas=self.canvas_command, x=330, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Tray Mode  ",  text_size=12, on_default=True)
        self.radio_point = RadioButton(canvas=self.canvas_command, x=440, y=50, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode",   text_size=12, on_default=False)
            # Set Tray Press Button
        self.press_pick  = PressButton(canvas=self.canvas_command, x=330, y=82,  w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Pick Tray", text_size=12, active_default=True)
        self.press_place = PressButton(canvas=self.canvas_command, x=330, y=112, w=200, h=24, r=12, active_color=Color.gray, inactive_color=Color.lightgray, text="Set Place Tray", text_size=12, active_default=True)
        self.jogging = False
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
        self.homing_x = False
            # Run Press Button
        self.press_run  = PressButton(canvas=self.canvas_command, x=655, y=90, w=128, h=44, r=22, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", text_size=22, active_default=False)
        self.running = False
        self.running_x = False
        # Section Seperator
        self.line_separate_1 = Line(canvas=self.canvas_command, point_1=(260, 20), point_2=(260, 140), width=2, color=Color.lightgray)
        self.line_separate_2 = Line(canvas=self.canvas_command, point_1=(595, 20), point_2=(595, 140), width=2, color=Color.lightgray)

        # Get Goal Point from Mouse Click in Point Mode 
        self.canvas_field.bind("<ButtonRelease-1>", self.mouse_position)

        # Get Out of Entry when Press Enter of Click Outside the Entry 
        self.bind("<Return>", self.out_entry)
        self.canvas_command.bind("<Button-1>", self.out_entry)
        
    def mouse_position(self, event):
        """
        This function is called when user click on the grid during point mode,
        then move the target and change entry text
        """
        if self.operation_mode == "Point" and self.connection:
            if not self.running and not self.homing and not self.jogging:
                # Convert Pixel to Grid
                grid_x, grid_y = self.grid.map_2D_to_3D(event.x, event.y)
                # Reduce to 1 decimal point
                self.point_target_x = self.round_value(grid_x)
                self.point_target_y = self.round_value(grid_y)
                # Move Target to Desired Grid Position
                self.target.move_to(self.point_target_x, self.point_target_y)
                # Set Text in Entry
                self.entry_x.set_text(self.point_target_x)
                self.entry_y.set_text(self.point_target_y)

    def round_value(self, value):
        """
        This function rounds value to 1 decimal digit (round up when >= .05)
        """
        # Remove blank space
        value = str(value).replace(" ", "")
        # Convert String to Float
        value = float(value)
        # Round
        if value >= 0:
            decimal_point = int(abs(value+0.0000000001) * 100) % 10
        else:
            decimal_point = int(abs(value-0.0000000001) * 100) % 10

        if decimal_point < 5:
            return int(value*10)/10
        else:
            if value >= 0:
                return int(value*10+1)/10
            else:
                return int(value*10-1)/10

    def out_entry(self, event):
        """
        This function is called when user click outside the entry or press enter
        """
        if self.operation_mode == "Point":
            self.focus()
            # Move Target according to Entry's value if value is normal 
            if self.validate_entry() == "Normal":
                # Convert String (Entry's value) to Float and Reduce to 1 decimal point
                self.point_target_x = self.round_value(self.entry_x_value)
                self.point_target_y = self.round_value(self.entry_y_value)
                # Set Entry Text
                self.entry_x.set_text(str(self.point_target_x))
                self.entry_y.set_text(str(self.point_target_y))
                # Move Target
                self.target.move_to(self.point_target_x, self.point_target_y)

    def validate_entry(self):
        """
        This function validates input in entry and show error message
        """
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
                self.press_run.deactivate()
            else:
                self.message_error.hide()
                if not self.running and not self.homing and not self.jogging and not self.gripping and self.connection and self.usb_connect and self.protocol_y.routine_normal:
                    self.press_run.activate()
            # Return Validation Result
            return validate_result

        else:
            self.message_error.hide()
            if self.show_tray_pick and self.show_tray_place:
                if not self.running and not self.homing and not self.jogging and not self.gripping:
                    self.press_run.activate()
            else:
                self.press_run.deactivate()
    
    def interpret_validate(self, validate_result, entry):
        """
        This function converts number code from validation result to error text
        """
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
        """
        This function turns on end-effector's laser with protocol, turn on laser toggle, show laser on UI's navigator
        """
        self.protocol_y.write_end_effector_status("Laser On")
        self.toggle_laser.turn_on()
    
    def turn_off_laser(self):
        """
        This function turns off end-effector's laser with protocol, turn off laser toggle, hide laser on UI's navigator
        """
        self.protocol_y.write_end_effector_status("Laser Off")
        self.toggle_laser.turn_off()

    def turn_on_gripper(self):
        """
        This function turns on end-effector's gripper with protocol, turn on gripper toggle, show laser messagebox
        """
        self.protocol_y.write_end_effector_status("Gripper Power On")
        self.toggle_gripper.turn_on()

    def turn_off_gripper(self):
        """
        This function turns off end-effector's gripper with protocol, turn off gripper toggle, hide laser messagebox
        """
        self.protocol_y.write_end_effector_status("Gripper Power Off")
        self.toggle_gripper.turn_off()

    def movement(self, grid_x, grid_y):
        self.navi.move_to(grid_x, grid_y)
        pixel_x, pixel_y = self.grid.map_3D_to_2D(grid_x, grid_y, self.navi.grid_z)
        if grid_x <= 0:
            # Message box = Navi's right
            self.message_navi.align = "Left"
            self.message_laser.align = "Left"
            self.message_navi.move_to (pixel_x+14, pixel_y-10)
            self.message_laser.move_to(pixel_x+14, pixel_y+38)
            self.message_navi.generate_tail_points()
            self.message_laser.generate_tail_points()
            self.message_navi.tail.recreate (self.message_navi.tail_points["NW"])
            self.message_laser.tail.recreate(self.message_laser.tail_points["SW"])
        else:
            # Message box = Navi's left
            self.message_navi.align = "Right"
            self.message_laser.align = "Right"
            self.message_navi.move_to (pixel_x-14, pixel_y-10)
            self.message_laser.move_to(pixel_x-14, pixel_y+38)
            self.message_navi.generate_tail_points()
            self.message_laser.generate_tail_points()
            self.message_navi.tail.recreate (self.message_navi.tail_points["NE"])
            self.message_laser.tail.recreate(self.message_laser.tail_points["SE"])

    def handle_toggle_laser(self):
        """
        This function handles when user press laser toggle
        """
        if self.toggle_laser.pressed:
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
        """
        This function handles when user press gripper toggle
        """
        if self.toggle_gripper.pressed:
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

        if self.connection and not self.running and not self.gripping:
            if self.toggle_gripper.on == False:
                self.press_arrow.deactivate()
            else:
                self.press_arrow.activate()

    def handle_press_arrow(self):
        """
        This function handles when user press arrow (pick/place) button
        """
        if self.press_arrow.pressed:
            if self.toggle_gripper.on: 
                if self.direction_arrow == "pick":
                    self.protocol_y.write_end_effector_status("Gripper Pick")
                    self.press_arrow.photo_arrow_pick.hide()
                    self.press_arrow.photo_arrow_place.show()
                    self.direction_arrow = "place"
                    self.press_arrow.change_text("     Place")
                elif self.direction_arrow == "place":
                    self.protocol_y.write_end_effector_status("Gripper Place")
                    self.press_arrow.photo_arrow_place.hide()
                    self.press_arrow.photo_arrow_pick.show()
                    self.direction_arrow = "pick"
                    self.press_arrow.change_text("     Pick")
                self.gripping = True
                self.toggle_laser.deactivate()
                self.toggle_gripper.deactivate()
                self.press_arrow.deactivate()
                self.press_pick.deactivate()
                self.press_place.deactivate()
                self.press_run.deactivate()
                self.press_home.deactivate()
                self.press_arrow.pressed = False

    def handle_radio_operation(self):
        """
        This function handles when user press radio button (choose operation mode)
        """
        # Click Point Mode
        if self.operation_mode == "Tray" and self.radio_point.on:
            self.radio_tray.turn_off()
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
        elif self.operation_mode == "Point" and self.radio_tray.on:
            self.radio_point.turn_off()
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
        """
        This function handles when user press "Set Pick Tray" button
        """
        if self.press_pick.pressed:
            # Close Gripper & Open Laser First
            if not self.toggle_laser.on:
                self.toggle_laser.pressed = True
                self.handle_toggle_laser()
            self.protocol_y.write_base_system_status("Set Pick Tray")
            self.tray_pick.clear_tray()
            self.jogging = True
            self.toggle_laser.deactivate()
            self.toggle_gripper.deactivate()
            self.press_arrow.deactivate()
            self.radio_tray.deactivate()
            self.radio_point.deactivate()
            self.press_pick.deactivate()
            self.press_place.deactivate()
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_pick.pressed = False

    def handle_press_tray_place(self):
        """
        This function handles when user press "Set Place Tray" button
        """
        if self.press_place.pressed:
            # Close Gripper & Open Laser First
            if not self.toggle_laser.on:
                self.toggle_laser.pressed = True
                self.handle_toggle_laser()
            self.protocol_y.write_base_system_status("Set Place Tray")
            self.tray_place.clear_tray()
            self.jogging = True
            self.toggle_laser.deactivate()
            self.toggle_gripper.deactivate()
            self.press_arrow.deactivate()
            self.radio_tray.deactivate()
            self.radio_point.deactivate()
            self.press_pick.deactivate()
            self.press_place.deactivate()
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_place.pressed = False

    def handle_press_home(self):
        """
        This function handles when user press "Home" button
        """
        if self.press_home.pressed:
            self.protocol_y.write_base_system_status("Home")
            self.homing = True
            # Close Laser
            if self.toggle_laser.on:
                self.turn_off_laser()
            # Close Gripper
            if self.toggle_gripper.on:
                self.turn_off_gripper()
            self.toggle_laser.deactivate()
            self.toggle_gripper.deactivate()
            self.press_arrow.deactivate()
            self.radio_tray.deactivate()
            self.radio_point.deactivate()
            self.press_pick.deactivate()
            self.press_place.deactivate()
            self.entry_x.disable()
            self.entry_y.disable()
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_home.pressed = False

    def handle_press_run(self):
        """
        This function handles when user press "Run" button
        """
        if self.press_run.pressed:
            if self.operation_mode == "Tray":
                self.protocol_y.write_base_system_status("Run Tray Mode")
            elif self.operation_mode == "Point":
                self.protocol_y.write_goal_point(self.point_target_x*10, self.point_target_y*10)
                self.protocol_y.write_base_system_status("Run Point Mode")
            self.running = True
            # Close Laser & Open Gripper First
            if not self.toggle_gripper.on:
                self.toggle_gripper.pressed = True
                self.handle_toggle_gripper()
            self.toggle_laser.deactivate()
            self.toggle_gripper.deactivate()
            self.press_arrow.deactivate()
            self.radio_tray.deactivate()
            self.radio_point.deactivate()
            self.press_pick.deactivate()
            self.press_place.deactivate()
            self.entry_x.disable()
            self.entry_y.disable()
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_run.pressed = False

    def handle_finish_moving(self):
        """
        This function handles when finish moving to reactivate elements
        """
        self.toggle_laser.activate()
        self.toggle_gripper.activate()
        self.press_arrow.activate()
        self.radio_tray.activate()
        self.radio_point.activate()
        self.press_pick.activate()
        self.press_place.activate()
        self.entry_x.enable()
        self.entry_y.enable()
        self.press_run.activate()
        self.press_home.activate()

    def handle_disconnected(self):
        """
        This function handles when connection miss a heartbeat
        """
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
        """
        This function handles when connection obtain a heartbeat again
        """
        self.message_connection.hide()
        self.text_x_pos_num.activate(self.text_x_pos_num.text, Color.blue)
        self.text_y_pos_num.activate(self.text_y_pos_num.text, Color.blue)
        self.text_y_spd_num.activate(self.text_y_spd_num.text, Color.blue)
        self.text_y_acc_num.activate(self.text_y_acc_num.text, Color.blue)
        if not self.running and not self.homing and not self.jogging:
            self.toggle_laser.activate()
            self.toggle_gripper.activate()
            # self.press_arrow.activate()
            self.press_pick.activate()
            self.press_place.activate()
            self.entry_x.enable()
            self.entry_y.enable()
            self.press_run.activate()
            self.press_home.activate()

    def handle_protocol_ui(self):
        """
        This function handles updating UI according to protocol status 
        """
        # Laser
        if self.protocol_y.laser_on == "1":
            self.navi.navigator_laser.show()
        else:
            self.navi.navigator_laser.hide()

        # Gripper
        if self.protocol_y.gripper_pick == "1":
            self.press_arrow.deactivate()
            self.message_laser.change_text("Gripper Pick")
            self.message_laser.show()
        elif self.protocol_y.gripper_place == "1":
            self.press_arrow.deactivate()
            self.message_laser.change_text("Gripper Place")
            self.message_laser.show()
        else:
            self.gripping = False
            self.message_laser.hide()
            if not self.jogging and not self.homing and not self.running:
                self.toggle_laser.activate()
                self.toggle_gripper.activate()
                if self.protocol_y.gripper_power == "1":
                    self.press_arrow.activate()

        # Actual motion value
        self.text_x_pos_num.change_text(self.protocol_x.x_axis_actual_pos)
        self.text_y_pos_num.change_text(self.protocol_y.y_axis_actual_pos)
        self.text_y_spd_num.change_text(self.protocol_y.y_axis_actual_spd)
        self.text_y_acc_num.change_text(self.protocol_y.y_axis_actual_acc)
        # Move navi
        self.movement(self.protocol_x.x_axis_actual_pos/10, self.protocol_y.y_axis_actual_pos/10)

        # Moving Status
        if self.protocol_y.y_axis_moving_status == "Idle":
            # Hide navi message
            self.message_navi.hide()
            # When finish moving
            if self.protocol_y.y_axis_moving_status_before != "Idle":
                self.handle_finish_moving()
                if self.protocol_y.y_axis_moving_status_before == "Jog Pick":
                    self.protocol_y.read_pick_tray_position()
                    self.tray_pick.origin_x = self.protocol_y.pick_tray_origin_x / 10
                    self.tray_pick.origin_y = self.protocol_y.pick_tray_origin_y / 10
                    self.tray_pick.orientation = self.protocol_y.pick_tray_orientation
                    self.tray_pick.create_tray()
                    self.jogging = False
                    self.show_tray_pick = True
                elif self.protocol_y.y_axis_moving_status_before == "Jog Place":
                    self.protocol_y.read_place_tray_position()
                    self.tray_place.origin_x = self.protocol_y.place_tray_origin_x / 10
                    self.tray_place.origin_y = self.protocol_y.place_tray_origin_y / 10
                    self.tray_place.orientation = self.protocol_y.place_tray_orientation
                    self.tray_place.create_tray()
                    self.jogging = False
                    self.show_tray_place = True
                elif self.protocol_y.y_axis_moving_status_before == "Home":
                    self.homing = False
                elif self.protocol_y.y_axis_moving_status_before == "Go Place":
                    self.running = False
                elif self.protocol_y.y_axis_moving_status_before == "Go Point":
                    self.running = False
                self.protocol_y.y_axis_moving_status_before = "Idle"
        else:
            # Show navi message
            if self.protocol_y.y_axis_moving_status == "Jog Pick":
                self.message_navi.change_text("Jogging")
            elif self.protocol_y.y_axis_moving_status == "Jog Place":
                self.message_navi.change_text("Jogging")
            elif self.protocol_y.y_axis_moving_status == "Home":
                self.message_navi.change_text("Homing")
            elif self.protocol_y.y_axis_moving_status == "Go Pick":
                self.message_navi.change_text("Going to Pick")
            elif self.protocol_y.y_axis_moving_status == "Go Place":
                self.message_navi.change_text("Going to Place")
            elif self.protocol_y.y_axis_moving_status == "Go Point":
                self.message_navi.change_text("Going to Point")
            self.message_navi.show()

    def handle_protocol_y(self):
        # Check USB connection
        if self.protocol_y.usb_connect:
            # When reconnect USB
            if self.protocol_y.usb_connect_before == False:
                self.handle_connected()
                self.protocol_y.usb_connect_before = True
            # Check if there is protocol error from user (y-axis)
            if self.protocol_y.routine_normal == False:
                self.message_connection.change_text("Protocol Error from Y-Axis")
                self.handle_disconnected()
            else:
                # Do protocol as normal every 200 ms
                if self.time_ms >= 200:
                    import time
                    start_time = time.time()
                    self.time_ms = 0
                    self.new_connection = self.protocol_y.heartbeat()
                    if self.new_connection: # If Connected
                        self.protocol_y.routine() # Do routine
                    end_time = time.time()
                    print((end_time-start_time)*1000, "ms\n")

                # If Connection is Changed 
                if self.connection != self.new_connection:
                    # Update Connection Value
                    self.connection = self.new_connection
                    if not self.connection: # If Disconnected
                        self.handle_disconnected()
                    else: # If Reconnected
                        self.handle_connected()
                # Update UI accoring to protocol status
                self.handle_protocol_ui()

        else:
            self.message_connection.change_text("Please Connect the USB")
            self.handle_disconnected()
            self.protocol_y.write_heartbeat()
            self.protocol_y.usb_connect_before = False

    def handle_protocol_x(self):
        # When start homing
        if self.protocol_y.x_axis_moving_status == "Home":
            if self.protocol_y.x_axis_moving_status_before == "Idle":
                self.protocol_x.write_x_axis_moving_status("Home")
                self.homing_x = True
        # When start running
        elif self.protocol_y.x_axis_moving_status == "Run":
            if self.protocol_y.x_axis_moving_status_before == "Idle":
                self.protocol_x.write_x_axis_moving_status("Run")
                # Then read target
                # Then write target
                self.running_x = True
        elif self.protocol_y.x_axis_moving_status == "Idle":
            # When stop homing
            if self.protocol_y.x_axis_moving_status_before == "Home":
                self.homing_x = False
            # When stop running
            if self.protocol_y.x_axis_moving_status_before == "Run":
                self.running_x = False
        # While homing or running
        if self.homing_x or self.running_x:
            self.protocol_x.read_holding_registers()
            self.protocol_x.read_x_axis_moving_status()
            self.protocol_x.read_x_axis_actual_motion()
            self.protocol_y.write_x_axis_moving_status(self.protocol_x.x_axis_moving_status)
            self.protocol_y.write_x_axis_actual_motion(self.protocol_x.x_axis_actual_pos, self.protocol_x.x_axis_actual_spd, self.protocol_x.x_axis_actual_acc)

if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()