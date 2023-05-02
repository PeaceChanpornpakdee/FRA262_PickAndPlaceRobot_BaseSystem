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
        binary_list = []
        while number > 0:
            binary_list.append(number % 2)
            number //= 2
        binary_list.reverse()
        binary_str = ''.join(str(bit) for bit in binary_list)
        if len(binary_str) < 8:
            binary_str = "0"*(8-len(binary_str)) + binary_str
        if end_digit == -1:
            if binary_str[start_digit] == "-":
                return binary_str[start_digit]
            else:
                return int(binary_str[start_digit])
        else:
            return binary_str[start_digit : end_digit+1]
        
    # def bit_wise_operate(self, register, max_len):
    #     data=[]
    #     for i in range(max_len):
    #         bit = (register>>i)&0x01
    #         data.append(bit)
    #     return data

    def heartbeat(self):
        # If read heartbeat as "Ya"
        if self.read_hearbeat() == 22881:
            # Write heartbeat as "Hi"
            self.write_heartbeat()
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

        print(self.base_system_status, self.y_axis_moving_status, self.x_axis_moving_status)

    def read_hearbeat(self):
        hearbeat_value = self.client.read_holding_registers(address=0x00, count=1, slave=self.slave_address).registers
        return hearbeat_value[0]
    
    def write_heartbeat(self):
        self.client.write_register(address=0x00, value=18537, slave=self.slave_address)

    def read_base_system_status(self):
        if self.get_binary_digit(self.register[0x01], 5) == 1:
            self.base_system_status = "Home"
        elif self.get_binary_digit(self.register[0x01], 6) == 1:
            self.base_system_status = "Run Tray Mode"
        elif self.get_binary_digit(self.register[0x01], 7) == 1:
            self.base_system_status = "Run Point Mode"
        else:
            self.base_system_status = "Idle"

    def read_end_effector_status(self):
        self.laser_on      = self.get_binary_digit(self.register[0x02], 0)
        self.gripper_power = self.get_binary_digit(self.register[0x02], 1)
        self.gripper_pick  = self.get_binary_digit(self.register[0x02], 2)
        self.gripper_place = self.get_binary_digit(self.register[0x02], 3)
        if self.gripper_pick and self.gripper_place:
            print('WARNING : GripperPicking and GripperPlacing are both working.')

    def read_y_axis_moving_status(self):
        if self.get_binary_digit(self.register[0x10], 5) == 1:
            self.y_axis_moving_status = "Jog"
        elif self.get_binary_digit(self.register[0x10], 6) == 1:
            self.y_axis_moving_status = "Go Pick"
        elif self.get_binary_digit(self.register[0x10], 7) == 1:
            self.y_axis_moving_status = "Go Place"
        else:
            self.y_axis_moving_status = "Idle"

    def read_x_axis_moving_status(self):
        if self.get_binary_digit(self.register[0x40], 6) == 1:
            self.x_axis_moving_status = "Home"
        elif self.get_binary_digit(self.register[0x40], 7) == 1:
            self.x_axis_moving_status = "Run"
        else:
            self.x_axis_moving_status = "Idle"