import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    (time, car_name, flags, gear, plid, speed, rpm,
    	turbo, eng_temp, fuel, oil_press, oil_temp, dash_lights, show_lights,
    	throttle, brake, clutch, disp1, disp2) = struct.unpack('I4shccfffffffIIfff16s16s', data[0:92])
    print ("%.2f %.2f %d - %.0f" % (fuel*100, throttle*100, speed*3.6, rpm))