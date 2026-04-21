from smbus import SMBus
import time


class SoilSensor:
    def __init__(self, dry=687, wet=444, address=0x4B, bus_num=1):
        self.dry = dry
        self.wet = wet
        self.address = address
        self.bus = SMBus(bus_num)

    def read_raw(self):
        rd = self.bus.read_word_data(self.address, 0)
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        return data >> 2

    def get_moisture(self):
        raw = self.read_raw()

        if raw < self.wet:
            moisture = 100.0
        else:
            moisture = (self.dry - raw) * 100.0 / (self.dry - self.wet)

        if moisture < 0:
            moisture = 0.0

        return round(moisture, 1)


# Test (kun hvis filen køres direkte)
if __name__ == "__main__":
    sensor = SoilSensor()

    while True:
        value = sensor.get_moisture()
        print("Fugtighed:", value, "%")
        time.sleep(1)


''' Sådan skal det bruges senere i app.py
from soil import SoilSensor

soil = SoilSensor()
value = soil.get_moisture()'''
