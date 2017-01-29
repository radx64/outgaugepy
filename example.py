from outgauge import *

carFuelTankCapacity = 45.0

lastTime = 0.0
lastSpeed = 0.0
lastFuel = 0.0
burnAvgPerHour = []
burnAvgPer100Km = []

def calculateWindowedAvg(data, valueToAdd):
    data.append(valueToAdd)
    dataLen = len(data)
    dataAvg = sum(data, 0.0) / dataLen

    if dataLen > 50:
        data[:] = data[1:50]

    return dataAvg


def processPacket(packet):
    sys.stdout.write("\r F:%6.5f T:%06.2f S:%03d G:%d R:%.0f  " % (packet.fuel*100,
        packet.throttle*100, packet.speed*3.6, int.from_bytes(packet.gear, byteorder='big'), packet.rpm))

    global lastTime
    global lastSpeed
    global lastFuel
    global burnAvgPerHour

    deltaTime = (packet.time - lastTime) / 1000.0
    deltaFuel = packet.fuel - lastFuel
    deltaFuelInLiters = deltaFuel * carFuelTankCapacity

    burnedFuelPerHour = deltaFuelInLiters * deltaTime * 1000 * 3600
    burnAvgPerHourValue = calculateWindowedAvg(burnAvgPerHour, burnedFuelPerHour)

    traveledDistance = packet.speed * deltaTime
    if traveledDistance > 0.0:
        burnedFuelPer100Km = -deltaFuelInLiters  * ((100 * 1000)  / traveledDistance) 
        burnAvgPer100KmValue = calculateWindowedAvg(burnAvgPer100Km, burnedFuelPer100Km)
    else:
        burnAvgPer100KmValue = 0.0

    sys.stdout.write(" Average fuel burn: %6.1f [L/h]  %6.1f [L/100km]                  " % (-burnAvgPerHourValue, burnAvgPer100KmValue))

    sys.stdout.flush()  

    lastTime = packet.time
    lastSpeed = packet.speed
    lastFuel = packet.fuel

UDP_IP = "127.0.0.1"
UDP_PORT = 9000

if __name__ == '__main__':
    outgauge = OutGauge(UDP_IP, UDP_PORT, processPacket)
    outgauge.connect()