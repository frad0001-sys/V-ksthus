import pigpio

class LEDController:
    def __init__(self, red_pin=12, blue_pin=13, freq=1000):
        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise Exception("Kunne ikke forbinde til pigpio daemon")

        self.red_pin = red_pin
        self.blue_pin = blue_pin

        # Sæt PWM frekvens
        self.pi.set_PWM_frequency(self.red_pin, freq)
        self.pi.set_PWM_frequency(self.blue_pin, freq)

        # Start slukket
        self.set_pwm(0, 0)

    def set_pwm(self, red_percent, blue_percent):
        # Rød: max 60%
        red_percent = max(0, min(60, red_percent))

        # Blå: max 77%
        blue_percent = max(0, min(77, blue_percent))

        # Konverter korrekt til 0–255
        red_val = int((red_percent / 60) * 255)
        blue_val = int((blue_percent / 77) * 255)

        self.pi.set_PWM_dutycycle(self.red_pin, red_val)
        self.pi.set_PWM_dutycycle(self.blue_pin, blue_val)

    def off(self):
        self.set_pwm(0, 0)
