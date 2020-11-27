import time
import RPi.GPIO as GPIO

class Driver:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        # TODO: second motor

        self.PIN_R_EN_1 = 12
        self.PIN_L_EN_1 = 16
        self.PIN_R_PWM_1 = 11
        self.PIN_L_PWM_1 = 15
        
        GPIO.setup(self.PIN_R_EN_1, GPIO.OUT)
        GPIO.setup(self.PIN_R_PWM_1, GPIO.OUT)
        GPIO.setup(self.PIN_L_EN_1, GPIO.OUT)
        GPIO.setup(self.PIN_L_PWM_1, GPIO.OUT)

        self.RPWM_1 = GPIO.PWM(self.PIN_R_PWM_1, 1e3)
        self.LPWM_1 = GPIO.PWM(self.PIN_L_PWM_1, 1e3)
        
        GPIO.output(self.PIN_R_EN_1, True)
        GPIO.output(self.PIN_L_EN_1, True)
        self.RPWM_1.start(0)
        self.LPWM_1.start(0)

    def go(self, throttle, steering):
        speed_left, speed_right = self.convert_split(throttle, steering)
        speed_left, speed_right = min(100, max(-100, speed_left)), min(100, max(-100, speed_right))

        self.RPWM_1.ChangeDutyCycle(speed_left if speed_left > 0 else 0)
        self.LPWM_1.ChangeDutyCycle(speed_left*-1 if speed_left < 0 else 0)

        # TODO: second motor

    def stop(self):
        self.go(0, 0)

    def cleanup(self):
        self.RPWM_1.stop()
        self.LPWM_1.stop()
        GPIO.cleanup()

    @classmethod
    def convert_split(cls, throttle, steering):
        # TODO: implement
        return throttle, throttle