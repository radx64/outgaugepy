from outgauge import *

def processPacket(packet):
    sys.stdout.write("\r F:%6.2f T:%06.2f S:%03d G:%d R:%.0f  " % (packet.fuel*100,
        packet.throttle*100, packet.speed*3.6, int.from_bytes(packet.gear, byteorder='big'), packet.rpm))
    sys.stdout.flush()  

UDP_IP = "127.0.0.1"
UDP_PORT = 9000

if __name__ == '__main__':
    outgauge = OutGauge(UDP_IP, UDP_PORT, processPacket)
    outgauge.connect()