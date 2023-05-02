from pymodbus.client import ModbusSerialClient as ModbusClient

class Protocol():
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

    def get_binary_digit(self, number, start_digit, end_digit=-1):
        # Convert base 10 to base 2
        binary_num = ""
        while number > 0:
            binary_num = str(number % 2) + binary_num
            number = number // 2
        # Fill to 8 digits
        if len(binary_num) < 8:
            binary_num = "0"*(8-len(binary_num)) + binary_num
        # Return single digit
        if end_digit == -1:
            if binary_num[start_digit] == "-":
                # Return as string for "-"
                return binary_num[start_digit]
            else:
                # Return as integer for number
                return int(binary_num[start_digit])
        # Return multiple digits
        else:
            return binary_num[start_digit : end_digit+1]

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

        self.write_end_effector_status("Laser Off")



    def read_hearbeat(self):
        hearbeat_value = self.client.read_holding_registers(address=0x00, count=1, slave=self.slave_address).registers
        return hearbeat_value[0]
    
    def write_heartbeat(self):
        self.client.write_register(address=0x00, value=18537, slave=self.slave_address)

    def read_base_system_status(self):
        if self.get_binary_digit(self.register[0x01], 0) == 1:
            self.base_system_status = "Set Pick Tray"
        elif self.get_binary_digit(self.register[0x01], 1) == 1:
            self.base_system_status = "Set Place Tray"
        elif self.get_binary_digit(self.register[0x01], 2) == 1:
            self.base_system_status = "Home"
        elif self.get_binary_digit(self.register[0x01], 3) == 1:
            self.base_system_status = "Run Tray Mode"
        elif self.get_binary_digit(self.register[0x01], 4) == 1:
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
        self.laser_on      = self.get_binary_digit(self.register[0x02], 0)
        self.gripper_power = self.get_binary_digit(self.register[0x02], 1)
        self.gripper_pick  = self.get_binary_digit(self.register[0x02], 2)
        self.gripper_place = self.get_binary_digit(self.register[0x02], 3)
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
        if self.get_binary_digit(self.register[0x10], 0) == 1:
            self.y_axis_moving_status = "Jog"
        elif self.get_binary_digit(self.register[0x10], 1) == 1:
            self.y_axis_moving_status = "Home"
        elif self.get_binary_digit(self.register[0x10], 2) == 1:
            self.y_axis_moving_status = "Go Pick"
        elif self.get_binary_digit(self.register[0x10], 3) == 1:
            self.y_axis_moving_status = "Go Place"
        elif self.get_binary_digit(self.register[0x10], 4) == 1:
            self.y_axis_moving_status = "Go Point"
        else:
            self.y_axis_moving_status = "Idle"

    def read_x_axis_moving_status(self):
        if self.get_binary_digit(self.register[0x40], 0) == 1:
            self.x_axis_moving_status = "Home"
        elif self.get_binary_digit(self.register[0x40], 1) == 1:
            self.x_axis_moving_status = "Run"
        else:
            self.x_axis_moving_status = "Idle"

    def read_y_axis_actual_motion(self):
        # self.y_axis_actual_pos = self.get_binary_digit(self.register[0x11], 7, )
        self.y_axis_actual_spd = 0
        self.y_axis_actual_acc = 0