import socket
from time import sleep
import ctypes

ELEV_HOME_START = b'ELEVATION HOME START'
ELEV_HOME_STOP = b'ELEVATION HOME STOP'
ELEV_SET = b'ELEVATION SET '
ELEV_GOTO = b'ELEVATION GOTO '
ELEV_STOP = b'ELEVATION STOP'
ELEV_STOP_RESET = b'ELEVATION STOP RESET'
ELEV_GET_POS = b'ELEVATION GET POSITION'
ELEV_GET_TARGET = b'ELEVATION GET'
ELEV_GET_FLAGS = b'ELEVATION GET FLAGS'
ELEV_GET_ALL = b'ELEVATION GET ALL'
    
    
class Elevation:
    def __init__(self, baudrate = 9600) -> None:
        self.elevation = 0
        self.target_position = 0
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
        try:
            self.socket.connect((self.ip_addr, self.port))
        except: 
            print('Failed to connect')
            
    def send_command(self, msg):
        recieved_msg = ''
        msg = msg + b'\n'
        print("sending", msg)
        self.socket.send(msg)
        
        sleep(0.5)
        
        while True:
            print("recving")
            buffer = self.socket.recv(256)
            print("bajs")
            if (buffer[len(buffer) - 1] == 10):
                recieved_msg += str(buffer)
                
                break

            if len(buffer) > 0:
                recieved_msg += str(buffer)
            else:
                break
        
        sleep(0.1)
        
        return recieved_msg

            
    def start_homing(self):
        msg = self.send_command(ELEV_HOME_START)
        
    def goto_absolute(self, position):
        msg = ELEV_GOTO + bytearray(str(position).encode('ascii'))
        self.send_command(msg)
        
    def get_position(self):
        msg = self.send_command(ELEV_GET_POS)
        print(msg)
    
    def stop(self):
        self.socket.close()
    
if __name__ == '__main__':
    elev = Elevation()
    elev.begin()
    #elev.start_homing()
    elev.goto_absolute(300)
    elev.get_position()
    #print(elev.send_command(ELEV_GET_ALL))""
    
    elev.stop()