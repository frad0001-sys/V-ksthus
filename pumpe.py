import pigpio
import time


class WaterPump:
    def __init__(self, pin=18):
        self.pin = pin
        self.pi = pigpio.pi()
        self.running = False

        # Sørg for pumpen er slukket ved start
        self.pi.write(self.pin, 0)

    def on(self):
        self.pi.write(self.pin, 1)
        self.running = True

    def off(self):
        self.pi.write(self.pin, 0)
        self.running = False

    def water(self, duration=3):
        self.on()
        time.sleep(duration)
        self.off()


# Test (kun hvis filen køres direkte)
if __name__ == "__main__":
    pump = WaterPump()

    try:
        while True:
            print("Vander i 3 sekunder...")
            pump.water(3)
            time.sleep(5)

    except KeyboardInterrupt:
        pump.off()
        print("Pump stoppet")

'''
from pumpe import WaterPump

pump = WaterPump()

pump.on()
pump.off()

# eller
pump.water(5)  # vander i 5 sek
'''
