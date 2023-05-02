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

        self.client= ModbusClient(method = "rtu", port=self.port,stopbits = 1, bytesize = 8, parity = 'E', baudrate= 19200)
        self.client.connect()
        print('Connection Status :', self.client.connect())

    def heartbeat(self):
        # If read heartbeat as "Ya"
        if self.read_hearbeat() == 22881:
            # Write heartbeat as "Hi"
            self.write_heartbeat()
            return True
        else:
            return False

    def routine(self):
        print("""Read
        Base System Status
        End Effector Status
        y-Axis Moving Status
        x-Axis Moving Status""")

    def read_hearbeat(self):
        hearbeat_value = self.client.read_holding_registers(address=0x00, count=1, slave=self.slave_address).registers
        return hearbeat_value[0]
    
    def write_heartbeat(self):
        self.client.write_register(address=0x00, value=18537, slave=self.slave_address)