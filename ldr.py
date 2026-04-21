import smbus
import time


class LDRSensor:
    def __init__(self, address=0x48, bus_num=1):
        self.address = address
        self.bus = smbus.SMBus(bus_num)

        # Kalibrering (justér hvis nødvendigt)
        self.darkAdc = 7
        self.brightAdc = 635

        # Lineær skalering
        self.a = (0 - 60) / (self.brightAdc - self.darkAdc)
        self.b = 60 - self.a * self.darkAdc

    def read_raw(self):
        data = self.bus.read_word_data(self.address, 0)
        data = ((data & 0xFF) << 8) | (data >> 8)
        return (data >> 2) & 0x03FF

    def get_light(self):
        adcVal = self.read_raw()

        # Beregn PWM værdier
        red = self.a * adcVal + self.b
        red = max(0, min(60, red))  # clamp 0–60%

        blue = red * 77 / 60

        # Bestem lysniveau
        if adcVal < 25:
            stage = "MØRKT"
        elif adcVal < 150:
            stage = "SVAGT LYS"
        elif adcVal < 400:
            stage = "NORMALT LYS"
        else:
            stage = "STÆRKT LYS"

        return {
            "adc": adcVal,
            "red": round(red, 2),
            "blue": round(blue, 2),
            "stage": stage
        }


# Test (kun hvis filen køres direkte)
if __name__ == "__main__":
    sensor = LDRSensor()

    while True:
        data = sensor.get_light()

        print(
            "ADC:", data["adc"],
            "| Stage:", data["stage"],
            "| Red PWM:", data["red"],
            "| Blue PWM:", data["blue"]
        )

        time.sleep(0.5)

'''Sådan skal det bruges senere i app.py
from ldr import LDRSensor

ldr = LDRSensor()
data = ldr.get_light()

print(data["adc"], data["stage"])
'''
