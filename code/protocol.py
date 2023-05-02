from pymodbus.client import ModbusSerialClient as ModbusClient

class Protocol_Y():
    """
    Protocol Class
    """
    def __init__(self, app):
        self.app = app
        self.port = "COM5"
        self.port = "/dev/cu.usbmodem14203"

        self.slave_address = 0x15
        self.register = []

        self.client= ModbusClient(method = "rtu", port=self.port,stopbits = 1, bytesize = 8, parity = 'E', baudrate= 19200)
        self.client.connect()
        print('Connection Status :', self.client.connect())

    def decimal_to_binary(self, decimal_num, start_digit, end_digit=-1):
        """
        This function converts base 10 to base 2
        """
        binary_num = ""
        while decimal_num > 0:
            binary_num = str(decimal_num % 2) + binary_num
            decimal_num = decimal_num // 2
        # Fill to 8 digits
        if len(binary_num) < 8:
            binary_num = "0"*(8-len(binary_num)) + binary_num
        # Return single digit
        if end_digit == -1:
            return int(binary_num[start_digit])
        # Return multiple digits
        else:
            return binary_num[start_digit : end_digit+1]
        
    def binary_to_decimal(self, binary_num):
        """
        This function converts base 2 to base 10
        """
        decimal_num = 0
        for i in range(len(binary_num)):
            decimal_num += int(binary_num[i]) * (2 ** (len(binary_num)-i-1))
        return decimal_num
        
    def heartbeat(self):
        if self.read_hearbeat() == 22881: # Read heartbeat as "Ya"
            self.write_heartbeat() # Write heartbeat as "Hi"
            return True
        else:
            # return False
            return True

    def routine(self):
        self.register = self.client.read_holding_registers(address=0x00, count=0x46, slave=self.slave_address).registers
        self.read_base_system_status()
        self.read_end_effector_status()
        self.read_y_axis_moving_status()
        self.read_x_axis_moving_status()

        print(self.base_system_status)
        print("Laser:", self.laser_on)
        print(self.y_axis_moving_status)
        print(self.x_axis_moving_status)
        print()


    def read_hearbeat(self):
        hearbeat_value = self.client.read_holding_registers(address=0x00, count=1, slave=self.slave_address).registers
        return hearbeat_value[0]
    
    def write_heartbeat(self):
        self.client.write_register(address=0x00, value=18537, slave=self.slave_address)

    def read_base_system_status(self):
        if self.decimal_to_binary(self.register[0x01], 0) == 1:
            self.base_system_status = "Set Pick Tray"
        elif self.decimal_to_binary(self.register[0x01], 1) == 1:
            self.base_system_status = "Set Place Tray"
        elif self.decimal_to_binary(self.register[0x01], 2) == 1:
            self.base_system_status = "Home"
        elif self.decimal_to_binary(self.register[0x01], 3) == 1:
            self.base_system_status = "Run Tray Mode"
        elif self.decimal_to_binary(self.register[0x01], 4) == 1:
            self.base_system_status = "Run Point Mode"
        else:
            self.base_system_status = "Idle"

    def write_base_system_status(self, command):
        if command == "Set Pick Tray":
            self.base_system_status_register = 0b10000000
        elif command == "Set Place Tray":
            self.base_system_status_register = 0b01000000
        elif command == "Home":
            self.base_system_status_register = 0b00100000
        elif command == "Run Tray Mode":
            self.base_system_status_register = 0b00010000
        elif command == "Run Point Mode":
            self.base_system_status_register = 0b00001000
        self.client.write_register(address=0x01, value=self.base_system_status_register, slave=self.slave_address)

    def read_end_effector_status(self):
        self.laser_on      = self.decimal_to_binary(self.register[0x02], 0)
        self.gripper_power = self.decimal_to_binary(self.register[0x02], 1)
        self.gripper_pick  = self.decimal_to_binary(self.register[0x02], 2)
        self.gripper_place = self.decimal_to_binary(self.register[0x02], 3)
        if self.gripper_pick and self.gripper_place:
            print('WARNING : GripperPicking and GripperPlacing are both working.')

    def write_end_effector_status(self, command):
        if command == "Laser On":
            self.end_effector_status_register = 0b10000000
        elif command == "Laser Off":
            self.end_effector_status_register = 0b00000000
        elif command == "Gripper Power On":
            self.end_effector_status_register = 0b01000000
        elif command == "Gripper Power Off":
            self.end_effector_status_register = 0b00000000
        elif command == "Gripper Pick":
            self.end_effector_status_register = 0b00100000
        elif command == "Gripper Place":
            self.end_effector_status_register = 0b00010000
        self.client.write_register(address=0x02, value=self.end_effector_status_register, slave=self.slave_address)

    def read_y_axis_moving_status(self):
        if self.decimal_to_binary(self.register[0x10], 0) == 1:
            self.y_axis_moving_status = "Jog"
        elif self.decimal_to_binary(self.register[0x10], 1) == 1:
            self.y_axis_moving_status = "Home"
        elif self.decimal_to_binary(self.register[0x10], 2) == 1:
            self.y_axis_moving_status = "Go Pick"
        elif self.decimal_to_binary(self.register[0x10], 3) == 1:
            self.y_axis_moving_status = "Go Place"
        elif self.decimal_to_binary(self.register[0x10], 4) == 1:
            self.y_axis_moving_status = "Go Point"
        else:
            self.y_axis_moving_status = "Idle"

    def read_y_axis_actual_motion(self):
        self.y_axis_actual_pos = self.decimal_to_binary(self.register[0x11], 1, 15)
        self.y_axis_actual_pos = self.binary_to_decimal(self.y_axis_actual_pos) / 10
        if self.decimal_to_binary(self.register[0x11], 0) == 1: # Negative digit
            self.y_axis_actual_pos = -self.y_axis_actual_pos
        self.y_axis_actual_spd = self.register[0x12] / 10
        self.y_axis_actual_acc = self.register[0x13] / 10

    def read_pick_tray_position(self):
        self.pick_tray_origin_x = self.decimal_to_binary(self.register[0x20], 1, 15)
        self.pick_tray_origin_x = self.binary_to_decimal(self.pick_tray_origin_x) / 10
        if self.decimal_to_binary(self.register[0x20], 0) == 1: # Negative digit
            self.pick_tray_origin_x = -self.pick_tray_origin_x
        self.pick_tray_origin_y = self.decimal_to_binary(self.register[0x21], 1, 15)
        self.pick_tray_origin_y = self.binary_to_decimal(self.pick_tray_origin_y) / 10
        if self.decimal_to_binary(self.register[0x21], 0) == 1: # Negative digit
            self.pick_tray_origin_y = -self.pick_tray_origin_y
        self.pick_tray_orientation = self.register[0x22] / 100

    def read_place_tray_position(self):
        self.place_tray_origin_x = self.decimal_to_binary(self.register[0x23], 1, 15)
        self.place_tray_origin_x = self.binary_to_decimal(self.place_tray_origin_x) / 10
        if self.decimal_to_binary(self.register[0x23], 0) == 1: # Negative digit
            self.place_tray_origin_x = -self.place_tray_origin_x
        self.place_tray_origin_y = self.decimal_to_binary(self.register[0x24], 1, 15)
        self.place_tray_origin_y = self.binary_to_decimal(self.place_tray_origin_y) / 10
        if self.decimal_to_binary(self.register[0x24], 0) == 1: # Negative digit
            self.place_tray_origin_y = -self.place_tray_origin_y
        self.place_tray_orientation = self.register[0x25] / 100

    def write_goal_point(self, x, y):
        self.goal_point_x_register = abs(x*10)
        if x < 0:
            self.goal_point_x_register += 0b1000000000000000
        self.goal_point_y_register = abs(y*10)
        if y < 0:
            self.goal_point_y_register += 0b1000000000000000
        self.client.write_register(address=0x30, value=self.goal_point_x_register, slave=self.slave_address)
        self.client.write_register(address=0x31, value=self.goal_point_y_register, slave=self.slave_address)

    def read_x_axis_moving_status(self):
        if self.decimal_to_binary(self.register[0x40], 0) == 1:
            self.x_axis_moving_status = "Home"
        elif self.decimal_to_binary(self.register[0x40], 1) == 1:
            self.x_axis_moving_status = "Run"
        else:
            self.x_axis_moving_status = "Idle"

    def write_x_axis_moving_status(self, command):
        if command == "Home":
            self.x_axis_moving_status_register = 0b10000000
        elif command == "Run":
            self.x_axis_moving_status_register = 0b01000000
        elif command == "Idle":
            self.x_axis_moving_status_register = 0x00
        self.client.write_register(address=0x46, value=self.x_axis_moving_status_register, slave=self.slave_address)

    def read_x_axis_target_motion(self):
        self.x_axis_target_pos = self.decimal_to_binary(self.register[0x41], 1, 15)
        self.x_axis_target_pos = self.binary_to_decimal(self.x_axis_target_pos) / 10
        if self.decimal_to_binary(self.register[0x41], 0) == 1: # Negative digit
            self.x_axis_target_pos = -self.x_axis_target_pos
        self.x_axis_target_spd = self.register[0x42] / 10
        self.x_axis_target_acc = self.register[0x43] / 10

    def write_x_axis_actual_motion(self):
        self.x_axis_actual_pos_register = self.decimal_to_binary(self.register[0x44], 1, 15)
        self.x_axis_actual_pos_register = self.binary_to_decimal(self.x_axis_actual_pos_register) / 10
        if self.decimal_to_binary(self.register[0x44], 0) == 1: # Negative digit
            self.x_axis_actual_pos_register = -self.x_axis_actual_pos_register
        self.x_axis_actual_spd_register = self.register[0x45] / 10
        self.x_axis_actual_acc_register = self.register[0x46] / 10
        self.client.write_register(address=0x44, value=self.x_axis_actual_pos_register, slave=self.slave_address)
        self.client.write_register(address=0x45, value=self.x_axis_actual_spd_register, slave=self.slave_address)
        self.client.write_register(address=0x46, value=self.x_axis_actual_acc_register, slave=self.slave_address)