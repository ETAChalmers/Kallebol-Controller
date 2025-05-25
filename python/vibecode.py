from flask import Flask, request, jsonify, render_template, redirect, url_for
import time
import threading
import pyads as pyadss
import logging

app = Flask(__name__)

azimuth = 0.0
elevation = 160.0
azimuth_act = 0.0
elevation_act = 0.0

clientnetid = "10.30.200.191.1.1" #Take your IP and add .1.1 to it
targetnetid = "5.79.241.154.1.1" #Find this in twincat
targetip = "10.30.200.73"
clientip = "10.30.200.191"
usrname = "Administrator"
password = "1"
routename = "kallebolNUC"

Next_ADS_command_allowed = 0
timeobj = time.gmtime(0) 

pyadss.set_local_address(clientnetid)
print("local ams set")
pyadss.add_route_to_plc(
    sending_net_id    =clientnetid, 
    adding_host_name  =clientip, 
    ip_address        =targetip, 
    username          =usrname, 
    password          =password, 
    route_name        =routename
    )
print("route added")
#pyadss.close_port()

print("time to open")
plc = pyadss.Connection(targetnetid, pyadss.PORT_TC3PLC1, targetip)
print("connection ----")
plc.open()
print("opened")
plc.set_timeout(10000)

try:
    plc.read_state() #Checks that we can read state, otherwise it's probably in config mode...
except:
    #PLC probably in config mode, terminating!
    exit()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def set_azimuth(value):
    global azimuth
    global Next_ADS_command_allowed
    if time.time_ns() > Next_ADS_command_allowed: 
        Next_ADS_command_allowed = time.time_ns() +300* (1000*1000) #in ms
        azimuth = max(-360.0, min(720.0, value))
        try:
            plc.write_by_name("MAIN.Azimuth.Azimuth_Target_Position_Parabola",azimuth)
        except:
            print("error setting Azimuth")
        print(f"[Motor] Azimuth set to {azimuth}°")


def set_elevation(value):
    global elevation
    global Next_ADS_command_allowed
    if time.time_ns() > Next_ADS_command_allowed: 
        Next_ADS_command_allowed = time.time_ns() +300* (1000*1000) #in ms
        elevation = max(0.0, min(200.0, value))
        try:
            plc.write_by_name("MAIN.Elevation.Targetpos_mm",elevation)
        except:
            print("error setting Elevation")
        print(f"[Motor] Elevation set to {elevation}")


@app.route('/')
def index():
    return render_template('index.html', azimuth=azimuth, elevation=elevation)


@app.route('/position', methods=['GET'])
def get_position():
    try:
        azimuth_act = plc.read_by_name("MAIN.Azimuth.HMI_Azimuth")
    except:
        print("error reading Azimuth")
    time.sleep(0.06)
    try:
        elevation_act = plc.read_by_name("MAIN.Elevation.Current_Position_mm")
    except:
        print("error reading Elevation")
    time.sleep(0.1) #there needs to be some sort of delay here it seems. since it is multi-threaded
    try:
        return jsonify({'azimuth_act': azimuth_act, 'elevation_act': elevation_act})
    except:
        print("error with the return of the ACT values in /Position for some reason")
        return jsonify({'azimuth_act': 0, 'elevation_act': 0})
    


@app.route('/move', methods=['POST'])
def move():
    direction = request.form.get('direction')
    step = 5
    if direction == 'left':
        set_azimuth(azimuth - step)
    elif direction == 'right':
        set_azimuth(azimuth + step)
    elif direction == 'up':
        set_elevation(elevation + step)
    elif direction == 'down':
        set_elevation(elevation - step)
    return redirect(url_for('index'))


def periodic_task():
    while True:
        # Do something here  e.g., simulate measurement, log, etc.
        
        print(f"[Loop] Current azimuth: {azimuth}°, elevation: {elevation}°")
        # Wait 1 second
        time.sleep(1)

# 🚀 Start background thread when Flask starts
def start_background_thread():
    thread = threading.Thread(target=periodic_task)
    thread.daemon = True  # Dies with the main thread
    thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)