import serial

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
