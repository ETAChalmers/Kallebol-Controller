import socket
import time

POSITION_TARGET_POSITION = [1111, 1]
POSITION_SPEED = [1111, 2]                  # POSITIONING SPEED
POSITION_ACCELERATION = [1111, 3]           # POSITIONING ACC
POSITION_DECCELARTION = [1111, 4]



STATUS_POSITION_ACTUAL = "680.5"
STATUS_POSITION_ERROR = "680.6"

STATUS_SPEED_ACTUAL = "681.5"
STATUS_SPEED_ERROR = "681.6"


STATUS_WORD_LOOKUP = [
    "Ready to switch on",
    "Switched on",
    "Operation enable",
    "Fault",
    "Voltage enabled",
    "Quick stop",
    "Switch On Disabled",
    "7",
    " =1: Speed=0 (drive motionless) ",
    "Remote",
    "Target reached",
    "Internal limit active",
    "Setpoint acknowledge(new setpoint is accepted)",
    "Following error",
    "0",
    "Registration found"
]


class Control_Word:
    def __init__(self) -> None:
        self.bit0 = 0
        self.bit1 = 0
        self.bit2 = 0
        self.bit3 = 0
        self.bit7 = 0
        
        self.new_set_point = 0
        self.change_set_imm = 0
        self.setting_of_pos_mode = 0
        self.stop = 0
        self.remote = 0
        self.endless = 0
        
        

    @property
    def word(self):
        self._word = (self.new_set_point << 4) + \
            (self.change_set_imm << 5) + \
            (self.setting_of_pos_mode << 6) + \
            (self.stop << 8) + \
            (self.remote << 11) + \
            (self.endless << 14) + \
            (self.bit1 << 1) + (self.bit2 << 2) + (self.bit3 << 3) + (self.bit7 << 7) + self.bit0
        #print("axis: ", self.energize_axis)
        #print("no_stop1", self.no_stop1)

        return self._word
    
    def enable_operation(self):
        self.bit0 = 0
        self.bit1 = 1
        self.bit2 = 1
        self.bit3 = 0
        self.bit7 = 0
        
    def start_operation(self):
        self.bit0 = 1
        self.bit1 = 1
        self.bit2 = 1
        self.bit3 = 1
        self.bit7 = 0
        

        
    def disable_operation(self):
        self.bit0 = 0
        self.bit1 = 0
        self.bit2 = 1
        self.bit3 = 1
        self.bit7 = 1
        
    def disable_voltage(self):
        self.bit0 = 0
        self.bit3 = 0
        
    def switch_on(self):
        self.bit0 = 1
        self.bit1 = 1
        self.bit2 = 1
        self.bit3 = 0
        self.bit7 = 0
        
    def quick_stop(self):
        self.bit0 = 0
        self.bit1 = 1
        self.bit2 = 0
        self.bit3 = 0
        self.bit7 = 0
        
    def disable_test(self):
        self.bit0 = 0
        self.bit7 = 0
        self.bit2 = 0
        self.bit3 = 0
        self.bit1 = 0
    
        
    @word.setter
    def word(self, value):
        self._word = value 


class Servo:
    def __init__(self, baudrate = 9600) -> None:
        self.current_position = 0
        self.target_position = 0
        
        self.control_word = Control_Word()
        self.control_word.change_set_imm = 1
        self.control_word.endless = 1

        self.speed = 0

        self.baudrate = baudrate 
        self.ip_addr = '192.168.30.143'
        self.port = 8886
        
        try:     
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('Failed to open socket on port %s', self.port)
        pass
    
    def begin(self):
        self.socket.connect((self.ip_addr, self.port))
        
        self.current_position = self.read_current_position()
        
    def energize(self):
        self.control_word.enable_operation()
        self.write_control_word(self.control_word)
        
        self.control_word.switch_on()
        self.write_control_word(self.control_word)
        
        self.control_word.start_operation()
        self.write_control_word(self.control_word)
        
    def denergize(self):
        self.control_word.disable_operation()
        self.write_control_word(self.control_word)
        
        
    def move_position(self, position):
        target_position = position - self.current_position
        
        self.write_object(1100, 6, target_position)
        
        self.control_word.new_set_point = 0
        self.write_control_word(self.control_word)
        self.control_word.new_set_point = 1
        self.write_control_word(self.control_word)
        
    def set_move_parameters(self):
        servo.write_object(1100, 14, 2000)
        servo.write_object(1111, 10, 50)
        servo.write_object(1111, 16, 50)
        
    def read_current_position(self):
        result = self.read_object(680, 8)
        result = int(result.split('\r')[0])
        
        return result
        
    def write_object(self, index, subindex, data):
        #print("Data: ", data)
        msg = b"O " + bytearray(str(index).encode('ascii')) + bytearray(".".encode('ascii')) + bytearray(str(subindex).encode('ascii')) + bytearray("=".encode('ascii')) + bytearray(str(data).encode('ascii')) + b'\r'
        #print(hex(data))
        #print(msg)
        self.socket.send(msg)
        recieved_msg = b''
        
        time.sleep(0.05)

        while True:
            #print("recving")
            buffer = self.socket.recv(256)
            #print("bajs")
            if (buffer.count(b'\r') > 0):
                recieved_msg += buffer
                break

            if len(buffer) > 0:
                recieved_msg += buffer

            else:
                break
        #print("Recv", recieved_msg)
        return bytes.decode(recieved_msg, encoding='ascii')

    def write_control_word(self, control_word):
        self.read_control_word()

        #print("Ssda: ", hex(control_word.word))
        #print(type(control_word.word))
        self.write_object(1100,3, control_word.word)

        time.sleep(0.5)
        #self.read_control_word()

    def read_control_word(self):
        print("++++++++++++ READ CONTROL WORD +++++++++++++++")
        recieved_control_word = self.read_object(1100, 3)

        for i in range(0, 16):
            print(str(i) + " : ", (int(recieved_control_word) >> i) & 1)


    def read_status_word(self):
        print("++++++++++ READ STATUS WORD ++++++++++++")
        recieved_control_word = self.read_object(1000, 3)
        #print(bin(int(recieved_control_word)))

        for i in range(0, 16):
            print(str(i) + " : " + STATUS_WORD_LOOKUP[i] + ": ", (int(recieved_control_word) >> i) & 1)

    def read_object(self, index, subindex):
        msg = b"O " + bytearray(str(index).encode('ascii')) + bytearray(".".encode('ascii')) + bytearray(str(subindex).encode('ascii')) + b'\r'
        #print(msg)
        self.socket.send(msg)
        
        time.sleep(0.05)
        
        print("MSG: ", len(msg))
        recieved_msg = b''
        
        while True:
            #print("recving")
            buffer = self.socket.recv(256)
            #print("bajs")
            if (buffer.count(b'\r') > 0):
                recieved_msg += buffer
                break

            if len(buffer) > 0:
                recieved_msg += buffer
            else:
                break
        
        print(recieved_msg)
        return bytes.decode(recieved_msg, encoding='ascii')
    
if __name__ == '__main__':
    servo = Servo()
    servo.begin()

    #servo.write_object(1111, 1, 1000000)
    servo.read_status_word()
    
    servo.write_object(1100, 6, 0)
    servo.write_object(1100, 14, 2000)
    servo.write_object(1111, 10, 50)
    servo.write_object(1111, 16, 50)
    
    control_word = Control_Word()
    control_word.endless = 1
    control_word.change_set_imm = 1
    control_word.remote = 0
    
    #control_word.quick_stop()
    
    control_word.stop = 0
    
    print(servo.read_object(2200, 2))
    
    """
    
    print(servo.read_object(1100, 5))
    
    
    control_word.enable_operation()
        
    servo.write_control_word(control_word=control_word)
    
    control_word.switch_on()
    
    servo.write_control_word(control_word=control_word)
    
    control_word.start_operation()
    
    servo.write_control_word(control_word=control_word)
    
    control_word.new_set_point = 0
    
    servo.write_control_word(control_word=control_word)
    

    
    
    servo.read_status_word()
    
    servo.write_object(1100, 6, 10000000)
    servo.write_object(1100, 14, 2000)
    servo.write_object(1111, 10, 50)
    servo.write_object(1111, 16, 50)
    
    control_word.new_set_point = 1
    
    servo.write_control_word(control_word=control_word)
    
    servo.write_control_word(control_word=control_word)
    time.sleep(1)
    servo.read_status_word()
    servo.read_control_word()
    
    
    servo.write_control_word(control_word=control_word)
    time.sleep(1)
    servo.read_status_word()
    servo.read_control_word()
    
    
    servo.write_object()

    print("DEMAND: ", servo.read_object(680, 4))

    print("============= SET TABLE =============")
    servo.write_object(1901, 1, 1)
    servo.write_object(1902, 1, 2000)
    servo.write_object(1904, 1, 50)
    servo.write_object(1905, 1, 1)
    servo.write_object(1906, 1, 500)
    servo.write_object(1907, 1, 500)
    servo.write_object(1908, 1, 10000)
    
    print(" ================ MOTION PROFILE TABLE ==========================")
    for i in range(1, 6):
        for j in range(1901, 1909):
            print("Row: " + str(j) + " Column: " + str(i) + " Data: " + servo.read_object(j, i))
            


    print("DEMAND: ", servo.read_object(680, 4))
    print("Actual: ", servo.read_object(680, 5))
    print("ERROR: ,", servo.read_object(550, 1))
    
    print("Temp: ", servo.read_object(85, 4))
    print("---------")
    print("---------")
    print("---------")
    print("---------")
    print("---------")
    

    control_word = Control_Word()
    

    print("=============== ACKLOGNE RROR")
    servo.write_control_word(control_word)

    control_word.no_stop2 = 1
    control_word.no_stop1 = 1
    control_word.energize_axis = 1
    control_word.start_edge = 0

    servo.write_control_word(control_word)

    control_word.address0 = 1
    
    servo.write_object(1100, 6, 1000000)

    servo.read_status_word()
    time.sleep(1)
    

    print("============= SET CONTROLWORD NO START EDGE =============")
    servo.write_control_word(control_word)

    servo.read_status_word()

    servo.read_control_word()

    time.sleep(1)
    print("============= SET CONTROLWORD WITH START EDGE =============")
    control_word.start_edge = 1
    servo.write_control_word(control_word)

    servo.read_status_word()

    print("---------")
    print("---------")
    print("---------")
    print("---------")
    print("---------")

    print("Demand Controller: ", servo.read_object(680, 12))
    print("Demand Value: ", servo.read_object(680, 4))
    print("Current positon: ", servo.read_object(680, 5))
    print("Acc: ", servo.read_object(1111,3))
    print("Dec: ", servo.read_object(1111,4))
    print("Speed: ", servo.read_object(1111,2))
    servo.read_control_word()
    
    time.sleep(10)
    control_word.energize_axis = 0
    control_word.no_stop2 = 0
    control_word.no_stop1 = 0
    print("============= SET CONTROLWORD WITH NO ENERGIZE =============")
    servo.write_control_word(control_word)

    servo.read_status_word()
    servo.read_control_word()
    #print(servo.read_object(1111, 1))
    
    #print(servo.read_object(685,2))
    """
        
    
    
