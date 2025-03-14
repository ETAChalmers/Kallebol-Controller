import socket
from time import sleep
import pyads as ads

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

MAX_HIGHEST = 0
MAX_LOWEST = 1100
    
class Elevation:
    def __init__(self, ip_addr, port, baudrate = 9600,) -> None:
        self.elevation = 0
        self.target_position = 0
        self.current_speed = 0
        
        self.baudrate = baudrate    
        self.ip_addr = "10.30.200.89"
        self.port = 2217

        self.client_netid = "5.146.142.192.1.1"
        print(self.client_netid)

        #ads.add_route(self.client_netid, self.ip_addr)

        self.connection = ads.Connection(self.client_netid, ads.PORT_TC3PLC1, self.ip_addr)

        """ 
        try:     
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('Failed to open socket on port %s', self.port)
        pass
        """
    
    def begin(self):
        try:
            #self.socket.connect((self.ip_addr, self.port))
            self.connection.open()

            print(self.connection.read_state())
        except Exception as e: 
            print('Failed to connect to linear actuator server:', e)
            
    def send_command(self, msg):
        recieved_msg = ''
        msg = msg + b'\n'
        print("sending", msg)
        self.socket.send(msg)
        
        sleep(0.1)
        
        while True:
            #print("recving")
            buffer = self.socket.recv(256)
            #print("bajs")
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
        print(msg)
        
    def goto_absolute(self, position):
        points = int(13.7*(87 - position))
        
        if points > MAX_LOWEST:
            points = MAX_LOWEST
        
        if points < MAX_HIGHEST:
            points = MAX_HIGHEST

        msg = ELEV_GOTO + bytearray(str(points).encode('ascii'))
        
        self.send_command(msg)
        
    def get_status(self):
        print(self.send_command(ELEV_GET_ALL))
        
    def get_position(self):
        msg = self.connection.read_by_name("MAIN.Elev_ENC_value")
        print(msg)
    
    def stop(self):
        self.socket.close()
    
if __name__ == '__main__':
    elev = Elevation(ip_addr="10.30.200.89", port=2217)
    elev.begin()
    elev.get_position()
    #elev.start_homing()
    #elev.goto_absolute(300)
    #elev.get_position()
    #print(elev.send_command(ELEV_GET_ALL))""
    
    #elev.stop()