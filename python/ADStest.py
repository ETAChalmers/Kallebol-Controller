import pyads as pyadss

clientnetid = "10.30.200.191.1.1" #Take your IP and add .1.1 to it
targetnetid = "5.79.241.154.1.1" #Find this in twincat
targetip = "10.30.200.73"
clientip = "10.30.200.191"
usrname = "Administrator"
password = "1"
routename = "kallebolNUC"

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

#print(plc.read_state())
plc.write_by_name("MAIN.Elevation.Targetpos_mm",150)
plc.write_by_name("MAIN.Azimuth.Azimuth_Target_Position_Parabola",180)
print(plc.read_by_name("MAIN.Azimuth.HMI_Azimuth"))