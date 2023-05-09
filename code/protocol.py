from pymodbus.client import ModbusSerialClient as ModbusClient

class Binary():
    """
    Binary Class
    """
    def decimal_to_binary(self, decimal_num):
        """
        This function converts base 10 to base 2
        """
        binary_num = ""
        while decimal_num > 0:
            binary_num = str(decimal_num % 2) + binary_num
            decimal_num = decimal_num // 2
        # Fill to 16 digits with 0
        if len(binary_num) < 16:
            binary_num = "0"*(16-len(binary_num)) + binary_num
        return binary_num
        
    def binary_to_decimal(self, binary_num):
        """
        This function converts base 2 to base 10
        """
        decimal_num = 0
        for i in range(len(binary_num)):
            decimal_num += int(binary_num[i]) * (2 ** (len(binary_num)-i-1))
        return decimal_num
    
    def binary_crop(self, digit, binary_num):
        """
        This function crops the last n digits of the binary number
        """
        return binary_num[len(binary_num)-digit:]

class Protocol_Y(Binary):
    """
    Protocol Y Class
    """
    def __init__(self):
        self.port = "COM5"
        self.port = "/dev/cu.usbmodem14203"

        self.slave_address = 0x15
        self.register = []

        self.laser_on = "0"
        self.gripper_pick = "0"
        self.gripper_place = "0"
        self.y_axis_moving_status_before = "Idle"
        self.y_axis_moving_status = "Idle"

        self.client= ModbusClient(method="rtu", port=self.port, stopbits=1, bytesize=8, parity="E", baudrate=19200)
        self.client.connect()
        print('Connection Status :', self.client.connect())
        
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
        # self.client.write_register(address=0x01, value=1, slave=self.slave_address)
        # self.client.write_register(address=0x02, value=1, slave=self.slave_address)
        # self.client.write_register(address=0x03, value=1, slave=self.slave_address)
        # self.client.write_register(address=0x04, value=1, slave=self.slave_address)

        print(self.base_system_status)
        print("Laser:", self.laser_on)
        print("Gripper Power:", self.gripper_power)
        print("Gripper Pick :", self.gripper_pick)
        print("Gripper Place:", self.gripper_place)
        print(self.y_axis_moving_status)
        print(self.x_axis_moving_status)


    def read_hearbeat(self):
        hearbeat_value = self.client.read_holding_registers(address=0x00, count=1, slave=self.slave_address).registers
        return hearbeat_value[0]
    
    def write_heartbeat(self):
        self.client.write_register(address=0x00, value=18537, slave=self.slave_address)

    def read_base_system_status(self):
        base_system_status_binary = self.binary_crop(5, self.decimal_to_binary(self.register[0x01]))
        if base_system_status_binary[0] == "1":
            self.base_system_status = "Set Pick Tray"
        elif base_system_status_binary[1] == "1":
            self.base_system_status = "Set Place Tray"
        elif base_system_status_binary[2] == "1":
            self.base_system_status = "Home"
        elif base_system_status_binary[3] == "1":
            self.base_system_status = "Run Tray Mode"
        elif base_system_status_binary[4] == "1":
            self.base_system_status = "Run Point Mode"
        else:
            self.base_system_status = "Idle"

    def write_base_system_status(self, command):
        if command == "Set Pick Tray":
            self.base_system_status_register = 0b10000
        elif command == "Set Place Tray":
            self.base_system_status_register = 0b01000
        elif command == "Home":
            self.base_system_status_register = 0b00100
        elif command == "Run Tray Mode":
            self.base_system_status_register = 0b00010
        elif command == "Run Point Mode":
            self.base_system_status_register = 0b00001
        self.client.write_register(address=0x01, value=self.base_system_status_register, slave=self.slave_address)

    def read_end_effector_status(self):
        end_effector_status_binary = self.binary_crop(4, self.decimal_to_binary(self.register[0x02]))
        self.laser_on      = end_effector_status_binary[0]
        self.gripper_power = end_effector_status_binary[1]
        self.gripper_pick  = end_effector_status_binary[2]
        self.gripper_place = end_effector_status_binary[3]

    def write_end_effector_status(self, command):
        if command == "Laser On":
            self.end_effector_status_register = 0b1000
        elif command == "Laser Off":
            self.end_effector_status_register = 0b0000
        elif command == "Gripper Power On":
            self.end_effector_status_register = 0b0100
        elif command == "Gripper Power Off":
            self.end_effector_status_register = 0b0000
        elif command == "Gripper Pick":
            self.end_effector_status_register = 0b0110
        elif command == "Gripper Place":
            self.end_effector_status_register = 0b0101
        self.client.write_register(address=0x02, value=self.end_effector_status_register, slave=self.slave_address)

    def read_y_axis_moving_status(self):
        self.y_axis_moving_status_before = self.y_axis_moving_status
        y_axis_moving_status_binary = self.binary_crop(5, self.decimal_to_binary(self.register[0x10]))
        if y_axis_moving_status_binary[0] == "1":
            self.y_axis_moving_status = "Jog Pick"
        elif y_axis_moving_status_binary[1] == "1":
            self.y_axis_moving_status = "Jog Place"
        elif y_axis_moving_status_binary[2] == "1":
            self.y_axis_moving_status = "Home"
        elif y_axis_moving_status_binary[3] == "1":
            self.y_axis_moving_status = "Go Pick"
        elif y_axis_moving_status_binary[4] == "1":
            self.y_axis_moving_status = "Go Place"
        elif y_axis_moving_status_binary[5] == "1":
            self.y_axis_moving_status = "Go Point"
        else:
            self.y_axis_moving_status = "Idle"

    def read_y_axis_actual_motion(self):
        y_axis_actual_pos_binary = self.decimal_to_binary(self.register[0x11])
        self.y_axis_actual_pos = self.binary_crop(15, y_axis_actual_pos_binary)
        self.y_axis_actual_pos = self.binary_to_decimal(self.y_axis_actual_pos) / 10
        if y_axis_actual_pos_binary[0] == "1":  # Negative digit
            self.y_axis_actual_pos = -self.y_axis_actual_pos
        self.y_axis_actual_spd = self.register[0x12] / 10
        self.y_axis_actual_acc = self.register[0x13] / 10

    def read_pick_tray_position(self):
        # Origin x
        pick_tray_origin_x_binary = self.decimal_to_binary(self.register[0x20])
        self.pick_tray_origin_x = self.binary_crop(15, pick_tray_origin_x_binary)
        self.pick_tray_origin_x = self.binary_to_decimal(self.pick_tray_origin_x) / 10
        if pick_tray_origin_x_binary[0] == "1": # Negative digit
            self.pick_tray_origin_x = -self.pick_tray_origin_x
        # Origin y
        pick_tray_origin_y_binary = self.decimal_to_binary(self.register[0x21])
        self.pick_tray_origin_y = self.binary_crop(15, pick_tray_origin_y_binary)
        self.pick_tray_origin_y = self.binary_to_decimal(self.pick_tray_origin_y) / 10
        if pick_tray_origin_y_binary[0] == "1": # Negative digit
            self.pick_tray_origin_y = -self.pick_tray_origin_y
        # Orientation
        self.pick_tray_orientation = self.register[0x22] / 100

    def read_place_tray_position(self):
        # Origin x
        place_tray_origin_x_binary = self.decimal_to_binary(self.register[0x23])
        self.place_tray_origin_x = self.binary_crop(15, place_tray_origin_x_binary)
        self.place_tray_origin_x = self.binary_to_decimal(self.place_tray_origin_x) / 10
        if place_tray_origin_x_binary[0] == "1": # Negative digit
            self.place_tray_origin_x = -self.place_tray_origin_x
        # Origin y
        place_tray_origin_y_binary = self.decimal_to_binary(self.register[0x24])
        self.place_tray_origin_y = self.binary_crop(15, place_tray_origin_y_binary)
        self.place_tray_origin_y = self.binary_to_decimal(self.place_tray_origin_y) / 10
        if place_tray_origin_y_binary[0] == "1": # Negative digit
            self.place_tray_origin_y = -self.place_tray_origin_y
        # Orientation
        self.place_tray_orientation = self.register[0x25] / 100

    def write_goal_point(self, x, y):
        self.goal_point_x_register = int(abs(x*10))
        if x < 0:
            self.goal_point_x_register += 0b1000000000000000
        self.goal_point_y_register = int(abs(y*10))
        if y < 0:
            self.goal_point_y_register += 0b1000000000000000
        self.client.write_register(address=0x30, value=self.goal_point_x_register, slave=self.slave_address)
        self.client.write_register(address=0x31, value=self.goal_point_y_register, slave=self.slave_address)

    def read_x_axis_moving_status(self):
        x_axis_moving_status_binary = self.binary_crop(2, self.decimal_to_binary(self.register[0x40]))
        if x_axis_moving_status_binary[0] == "1":
            self.x_axis_moving_status = "Home"
        elif x_axis_moving_status_binary[1] == "1":
            self.x_axis_moving_status = "Run"
        else:
            self.x_axis_moving_status = "Idle"

    def write_x_axis_moving_status(self, command):
        if command == "Home":
            self.x_axis_moving_status_register = 0b10
        elif command == "Run":
            self.x_axis_moving_status_register = 0b01
        elif command == "Idle":
            self.x_axis_moving_status_register = 0b00
        self.client.write_register(address=0x46, value=self.x_axis_moving_status_register, slave=self.slave_address)

    def read_x_axis_target_motion(self):
        x_axis_target_pos_binary = self.decimal_to_binary(self.register[0x41])
        self.x_axis_target_pos = self.binary_crop(15, x_axis_target_pos_binary)
        self.x_axis_target_pos = self.binary_to_decimal(self.x_axis_target_pos) / 10
        if x_axis_target_pos_binary[0] == "1": # Negative digit
            self.x_axis_target_pos = -self.x_axis_target_pos
        self.x_axis_target_spd = self.register[0x42] / 10
        self.x_axis_target_acc = self.register[0x43] / 10

    def write_x_axis_actual_motion(self, pos, spd, acc):
        self.x_axis_actual_pos_register = abs(pos*10)
        if pos < 0:
            self.x_axis_actual_pos_register += 0b1000000000000000
        self.x_axis_actual_spd_register = spd * 10
        self.x_axis_actual_acc_register = acc * 10
        self.client.write_register(address=0x44, value=self.x_axis_actual_pos_register, slave=self.slave_address)
        self.client.write_register(address=0x45, value=self.x_axis_actual_spd_register, slave=self.slave_address)
        self.client.write_register(address=0x46, value=self.x_axis_actual_acc_register, slave=self.slave_address)


class Protocol_X(Binary):
    """
    Protocol X Class
    """
    def __init__(self):
        self.port = "COM6"
        self.port = "/dev/cu.usbmodem14103"

        self.slave_address = 0x16
        self.register = []

        self.x_axis_moving_status_before = "Idle"
        self.x_axis_moving_status = "Idle"

        # self.client= ModbusClient(method="rtu", port=self.port, stopbits=1, bytesize=8, parity="E", baudrate=19200)
        # self.client.connect()

    # def read_holding_registers(self):
    #     self.register = self.client.read_holding_registers(address=0x00, count=0x06, slave=self.slave_address).registers

    def write_x_axis_moving_status(self, command):
        if command == "Home":
            self.x_axis_moving_status_register = 0b10
        elif command == "Run":
            self.x_axis_moving_status_register = 0b01
        self.client.write_register(address=0x00, value=self.x_axis_moving_status_register, slave=self.slave_address)

    def read_x_axis_moving_status(self):
        x_axis_moving_status_binary = self.binary_crop(2, self.decimal_to_binary(self.register[0x00]))
        if x_axis_moving_status_binary[0] == "1":
            self.x_axis_moving_status = "Home"
        elif x_axis_moving_status_binary[1] == "1":
            self.x_axis_moving_status = "Run"
        else:
            self.x_axis_moving_status = "Idle"

    def read_x_axis_actual_motion(self):
        x_axis_actual_pos_binary = self.decimal_to_binary(self.register[0x01])
        self.x_axis_actual_pos = self.binary_crop(15, x_axis_actual_pos_binary)
        self.x_axis_actual_pos = self.binary_to_decimal(self.x_axis_actual_pos) / 10
        if x_axis_actual_pos_binary[0] == "1":  # Negative digit
            self.x_axis_actual_pos = -self.x_axis_actual_pos
        self.x_axis_actual_spd = self.register[0x02] / 10
        self.x_axis_actual_acc = self.register[0x03] / 10

    def write_x_axis_target_motion(self, pos, spd, acc):
        self.x_axis_target_pos_register = abs(pos*10)
        if pos < 0:
            self.x_axis_target_pos_register += 0b1000000000000000
        self.x_axis_target_spd_register = spd * 10
        self.x_axis_target_acc_register = acc * 10
        self.client.write_register(address=0x04, value=self.x_axis_target_pos_register, slave=self.slave_address)
        self.client.write_register(address=0x05, value=self.x_axis_target_spd_register, slave=self.slave_address)
        self.client.write_register(address=0x06, value=self.x_axis_target_acc_register, slave=self.slave_address)  
        