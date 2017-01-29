import socket
import struct
import sys

class OutGaugePacket:
    def __init__(self, data):
        (self.time,
        self.car_name,
        self.flags,
        self.gear,
        self.plid,
        self.speed,
        self.rpm,
        self.turbo,
        self.eng_temp,
        self.fuel,
        self.oil_press,
        self.oil_temp,
        self.dash_lights,
        self.show_lights,
        self.throttle,
        self.brake,
        self.clutch,
        self.disp1,
        self.disp2) = struct.unpack('I4shccfffffffIIfff16s16s', data[0:92])

class OutGauge:

    def __init__(self, ip, port, callback):
        self.ip = ip
        self.port = port
        self.callback = callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        self.sock.bind((self.ip, self.port))
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            packet = OutGaugePacket(data)
            self.callback(packet)