from elevation import Elevation
from servo import Servo
import time
import numpy as np
from datetime import datetime

#from radio import Radio

STEP = 1
GOTO_FAIL_TRESHHOLD = 10000 # 100ms per point

class Kallebol:
    def __init__(self) -> None:
        self.azimuth = 0            # Degrees
        self.elevation = 0          # Degrees
        
        self.latitude = 0
        self.longitude = 0

        self.servo_ip_addr = "192.168.30.150"
        self.servo_port = 8886

        self.elev_ip_addr = '192.168.30.169'
        self.elev_port = 2217
        
        self.linear_actuatator = Elevation(ip_addr=self.elev_ip_addr, port=self.elev_port)
        self.servo = Servo(ip_addr = self.servo_ip_addr, port = self.servo_port)
        #self.radio = Radio()

    def test(moj):
        print(moj)
        print("Hello")

    def begin(self):
        self.servo.begin()
        
        self.linear_actuatator.begin()
        #self.linear_actuatator.start_homing()
    
    def go_home(self):
        self.goto_position(0, 0)
    
    def find_sun(self):
        pass
    
    def goto_position(self, azimuth, elevation):
        self.linear_actuatator.goto_absolute(elevation)
        self.servo.move_azimuth(azimuth)
        
        counter = 0
        while counter < GOTO_FAIL_TRESHHOLD:
            current_elevation = 0#87 - (self.linear_actuatator.get_position()/13.7)
            
            current_azimuth = float(self.servo.read_current_position())/840
            
            print("Current elevation: ", current_elevation)
            print("Current azimuth: ", current_azimuth)
            print("Counter: ", counter)
            
            if current_azimuth < azimuth + 0.05 and current_azimuth > azimuth - 0.05:
                print("Reached")
                return True
            
            time.sleep(0.1)
            counter += 1
            
        return False
    
    def move_servo(self, azimuth):
        self.servo.move_azimuth(azimuth)
    
    def sweep(self, min_elev, max_elev, steps_elev, min_azi, max_azi, steps_azi):
        going_right = True
        
        map = np.zeros((steps_elev, steps_azi))
        
        for x, elevation in enumerate(np.linspace(min_elev, max_elev, steps_elev)):
            if going_right == True:
                for y, azimuth in enumerate(np.linspace(min_azi, max_azi, steps_azi)):
                    print("Azimuth: ", azimuth)
                    print("Elevation: ", elevation)
                    if(not self.goto_position(azimuth, elevation)):
                        print("Failed to go to position. It timed out")
                        return False
                    
                    time.sleep(0.1)
                    map[x][y] = self.radio.average_power()
                    print(map)                    
                going_right = False
                
            else:
                for y, azimuth in enumerate(np.linspace(max_azi, min_azi, steps_azi)):
                    print("Azimuth: ", azimuth)
                    print("Elevation: ", elevation)
                    
                    if(not self.goto_position(azimuth, elevation)):
                        print("Failed to go to position. It timed out")
                        return False
                    
                    time.sleep(0.1)
                    map[x][-y - 1] = self.radio.average_power()
                    print(map)
                
                going_right = True
                
        file_name = datetime.now()
        file_name = file_name.strftime("map-%Y-%m-%d-%H_%M_%S.npy")
        with open(file_name, 'wb') as file:
            np.save(file, map)
            
        return map
