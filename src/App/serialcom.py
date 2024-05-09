import serial
import serial.tools.list_ports

# serial communication class
class CSerial:
    def __init__(self, port):
        self.m_ser = serial.Serial()
        self.m_ser.port = port
        self.m_ser.baudrate = 9600
        self.m_ser.timeout = 1
        try:
            self.m_ser.open()
        except:
            raise Exception("could not initialize serial connection")
        
    def readData(self):
        return self.m_ser.readline().decode("utf-8")
    
    def writeData(self, data):
        self.m_ser.write(bytes(data, 'ASCII'))

    def close(self):
        self.m_ser.close()

# returns chosen serial port name
def serialPortList():
    ports = serial.tools.list_ports.comports()
    portStr = []
    while True:
        print("\n-----\n")
        num = 0
        for port, desc, hwid in sorted(ports):
            print(f"{num}: {port}: {desc}")
            portStr.append(str(port))
            num += 1
        num -= 1
        try:
            choice = int(input(f"Select serial port by number 0 to {num}: "))
        except ValueError: print("Invalid number!"); continue
        if choice > num or choice < 0 or type(choice) is not int: print("Invalid number!"); continue
        else: break 

    return portStr[choice]