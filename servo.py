import socket

POSITION_TARGET_POSITION = [1111, 1]
POSITION_SPEED = [1111, 2]                  # POSITIONING SPEED
POSITION_ACCELERATION = [1111, 3]           # POSITIONING ACC
POSITION_DECCELARTION = [1111, 4]

STATUS_POSITION_ACTUAL = "680.5"
STATUS_POSITION_ERROR = "680.6"

STATUS_SPEED_ACTUAL = "681.5"
STATUS_SPEED_ERROR = "681.6"

class Servo:
    def __init__(self, baudrate = 9600) -> None:
        self.azimuth = 0
        self.target_position = 0
        self.current_position = 0

        self.current_speed = 0
        
        self.baudrate = baudrate 
        self.ip_addr = '192.168.30.169'
        self.port = 2217
        try:     
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('Failed to open socket on port %s', self.port)
        pass
    
    def begin(self):
        self.socket.connect((self.ip_addr, self.port))
        self.socket.recv(256)
    def test(self):
        self.socket.send(b'baj')

    
        
    
    
