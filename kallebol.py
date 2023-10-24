from elevation import Elevation
from servo import Servo

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
        
        self.linear_actuatator.start_homing()
    
    def go_home(self):
        pass
    
    def find_sun(self):
        pass
    
    def goto_position(self, azimuth, elevation):
        pass