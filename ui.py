import RPi.GPIO as GPIO
from threading import Thread, Timer
from time import sleep

class PINOUT:
    GREEN = 3
    YELLOW = 2
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
        self.blink_timeout = .5
        self.blink_repeat_timeout = 2
        self.blink_array = [False, False, False]
        self.blink_repeat = [False, False, False]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.yellow, GPIO.OUT)
        GPIO.setup(self.red, GPIO.OUT)
        self.reset_all()
        self.blink(True)

    def reset_all(self):
        self.reset_green()
        self.reset_yellow()
        self.reset_red()

    def reset_green(self):
        GPIO.output(self.green, GPIO.LOW)

    def reset_yellow(self):
        GPIO.output(self.yellow, GPIO.LOW)

    def reset_red(self):
        GPIO.output(self.red, GPIO.LOW)

    def set_green(self):
        GPIO.output(self.green, GPIO.HIGH)

    def set_yellow(self):
        GPIO.output(self.yellow, GPIO.HIGH)

    def set_red(self):
        GPIO.output(self.red, GPIO.HIGH)

    def reset_blink_green(self):
        self.blink_array[0] = False
        self.blink_repeat[0] = False

    def reset_blink_yellow(self):
        self.blink_array[1] = False
        self.blink_repeat[1] = False

    def reset_blink_red(self):
        self.blink_array[2] = False
        self.blink_repeat[2] = False

    def set_blink_green(self, repeat=False):
        self.blink_array[0] = True
        self.blink_repeat[0] = repeat

    def set_blink_yellow(self, repeat=False):
        self.blink_array[1] = True
        self.blink_repeat[1] = repeat

    def set_blink_red(self, repeat=False):
        self.blink_array[2] = True
        self.blink_repeat[2] = repeat

    def blink(self, state):
        if state:
            if self.blink_array[0]:
                GPIO.output(self.green, GPIO.HIGH)
            if self.blink_array[1]:
                GPIO.output(self.yellow, GPIO.HIGH)
            if self.blink_array[2]:
                GPIO.output(self.red, GPIO.HIGH)
            blink_timer = Timer(self.blink_timeout, self.blink, [False]) 
            blink_timer.start() 
        else: 
            GPIO.output(self.green, GPIO.LOW)
            GPIO.output(self.yellow, GPIO.LOW)
            GPIO.output(self.red, GPIO.LOW)
            self.blink_array[0] = self.blink_repeat[0]
            self.blink_array[1] = self.blink_repeat[1]
            self.blink_array[2] = self.blink_repeat[2]
            blink_timer = Timer(self.blink_repeat_timeout, self.blink, [True])
            blink_timer.start()
