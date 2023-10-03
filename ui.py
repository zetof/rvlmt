import RPi.GPIO as GPIO
from threading import Thread
from time import sleep

class PINOUT:
    GREEN = 2
    YELLOW = 3
    RED = 7
    SWITCH = 8

class Switch(Thread):
    def __init__(self, callback=None, pinout=PINOUT):
        self.switch = pinout.SWITCH
        self.callback = callback
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN)
        self.running = True
        Thread.__init__(self)

    def set_callback(self, callback):
        self.callback = callback

    def run(self):
        while self.running:
            if not GPIO.input(self.switch) and self.callback:
                self.callback()
            sleep(.1)

    def stop(self):
        self.running = False

class LEDS:
    def __init__(self, pinout=PINOUT):
        self.green = pinout.GREEN
        self.yellow = pinout.YELLOW
        self.red = pinout.RED
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.yellow, GPIO.OUT)
        GPIO.setup(self.red, GPIO.OUT)
        self.reset()

    def reset(self):
        GPIO.output(self.green, GPIO.LOW)
        GPIO.output(self.yellow, GPIO.LOW)
        GPIO.output(self.red, GPIO.LOW)

    def set(self):
        GPIO.output(self.green, GPIO.HIGH)
        GPIO.output(self.yellow, GPIO.HIGH)
        GPIO.output(self.red, GPIO.HIGH)
