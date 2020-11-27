import time
import RPi.GPIO as GPIO
from threading import Thread

from motorlib.driver import Driver
from bridge.bridge import Bridge

# Example usage:
# mosquitto_pub -t rccrate/control/throttle -m "55"
# mosquitto_pub -t rccrate/control/steering -m "-25"

class Main:
    def __init__(self, poll_freq=10):
        self.poll_freq = poll_freq
    
        # Init motor driver and GPIO
        self.driver = Driver()
        self.control = (0, 0,)
        
        self.PIN_IN = 3
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_IN, GPIO.IN)
        GPIO.add_event_detect(self.PIN_IN, GPIO.FALLING, callback=lambda _: self.toggle(), bouncetime=200)

        # Init communication bridge
        self.bridge = Bridge()
        self.bridge.connect()
        
    def toggle(self):
        pass

    def step(self):
        throttle = self.bridge.get_handler('control/throttle').get_latest()
        steering = self.bridge.get_handler('control/steering').get_latest()
        control = (throttle, steering,)
        
        if control != self.control:
            print(f'[debug] Setting control to {control}')
            self.control = control
            self.driver.go(*control)

    def poll(self):
        while True:
            time.sleep(1/self.poll_freq)
            self.step()

    def run(self):
        t = Thread(target=self.poll, daemon=True)
        t.start()
    
        while True:
            if input() == '':
                break

        self.driver.stop()
        self.driver.cleanup()

if __name__ == '__main__':
    main = Main()
    main.run()