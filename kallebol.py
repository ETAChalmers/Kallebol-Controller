from elevation import Elevation
from servo import Servo
import time
import numpy as np

from radio import Radio

STEP = 1

class Kallebol:
    def __init__(self) -> None:
        self.azimuth = 0            # Degrees
        self.elevation = 0          # Degrees
        
        self.latitude = 0
        self.longitude = 0

        self.linear_actuatator = Elevation()
        self.servo = Servo()
        self.radio = Radio()

    def begin(self):
        self.servo.begin()
        
        self.linear_actuatator.begin()
        #self.linear_actuatator.start_homing()
    
    def go_home(self):
        pass
    
    def find_sun(self):
        pass
    
    def goto_position(self, azimuth, elevation):
        self.linear_actuatator.goto_absolute(elevation)
        self.servo.move_azimuth(azimuth)
        
        counter = 0
        while counter < 200:
            current_elevation = 0#87 - (self.linear_actuatator.get_position()/13.7)
            
            current_azimuth = float(self.servo.read_current_position())/840
            
            print("Current elevation: ", current_elevation)
            print("Current azimuth: ", current_azimuth)
            print("Counter: ", counter)
            
            if current_azimuth < azimuth + 0.1 and current_azimuth > azimuth - 0.1:
                print("Reached")
                break
            
            time.sleep(0.5)
            counter += 1
    
    def sweep(self, min_elev, max_elev, steps_elev, min_azi, max_azi, steps_azi):
        going_right = True
        
        map = np.zeros((steps_elev, steps_azi))
        
        for x, elevation in enumerate(np.linspace(min_elev, max_elev, steps_elev)):
            if going_right == True:
                for y, azimuth in enumerate(np.linspace(min_azi, max_azi, steps_azi)):
                    print("Azimuth: ", azimuth)
                    print("Elevation: ", elevation)
                    self.goto_position(azimuth, elevation)
                    
                    time.sleep(1)
                    map[x][y] = self.radio.average_power()
                    print(map)                    
                going_right = False
                
            else:
                for y, azimuth in enumerate(np.linspace(max_azi, min_azi, steps_azi)):
                    print("Azimuth: ", azimuth)
                    print("Elevation: ", elevation)
                    
                    self.goto_position(azimuth, elevation)
                    time.sleep(1)
                    map[x][-y] = self.radio.average_power()
                    print(map)
                
                going_right = True
        with open('map.npy', 'wb') as file:
            np.save(file, map)
            
        return map