from elevation import Elevation
from servo import Servo
import time

STEP = 1

class Kallebol:
    def __init__(self) -> None:
        self.azimuth = 0            # Degrees
        self.elevation = 0          # Degrees
        
        self.latitude = 0
        self.longitude = 0

        self.linear_actuatator = Elevation()
        self.servo = Servo()

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
        self.servo.move_position(azimuth)
        
        counter = 0
        while counter < 100:
            current_elevation = self.linear_actuatator.get_position()
            current_azimuth = float(self.servo.read_current_position())
            
            print("Current elevation: ", current_elevation)
            print("Current azimuth: ", current_azimuth)
            
            if current_azimuth < azimuth + 5.0 and current_azimuth > azimuth - 5.0:
                print("Reached")
                break
            
            time.sleep(1)
            counter += 1
    
    def sweep(self, min_elev, max_elev, step_elev, min_azi, max_azi, step_azi):
        going_right = True
        
        for elevation in range(min_elev, max_elev, step_elev):
            if going_right == True:
                for azimuth in range(min_azi, max_azi, step_azi):
                    self.goto_position(azimuth, elevation)
                going_right = False
                
            else:
                for azimuth in range(max_azi, min_azi, step_azi):
                    self.goto_position(azimuth, elevation)
                
                going_right = True
            