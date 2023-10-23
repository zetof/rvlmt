from datetime import datetime
import locale
import time
from threading import Timer
import RPi.GPIO as GPIO

class PINOUT:
    BACK_LIGHT = 17
    ENABLE = 22
    RS = 27
    D4 = 25
    D5 = 24
    D6 = 23
    D7 = 18

class LCD16X2:

    BLANK_LINE = " " * 16

    def __init__(self, pinout=PINOUT):
        self.display_time = ""
        self.display_date = ""
        self.bl = pinout.BACK_LIGHT
        self.en = pinout.ENABLE
        self.rs = pinout.RS
        self.d4 = pinout.D4
        self.d5 = pinout.D5
        self.d6 = pinout.D6
        self.d7 = pinout.D7
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.bl, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.d4, GPIO.OUT)
        GPIO.setup(self.d5, GPIO.OUT)
        GPIO.setup(self.d6, GPIO.OUT)
        GPIO.setup(self.d7, GPIO.OUT)
        self.reset()
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

    def msleep(self, ms):
        time.sleep(ms / 1000)

    def usleep(self, us):
        time.sleep(us / 1000000)

    def set_pin(self, pin, val):
        if val == 0:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)

    def enable_pulse(self):
        self.set_pin(self.en, 1)
        self.usleep(40)
        self.set_pin(self.en, 0)
        self.usleep(40)

    def write_byte(self, data):
        self.set_pin(self.d4, (data & 0b00010000) >>4)
        self.set_pin(self.d5, (data & 0b00100000) >>5)
        self.set_pin(self.d6, (data & 0b01000000) >>6)
        self.set_pin(self.d7, (data & 0b10000000) >>7)
        self.enable_pulse()
       
        self.set_pin(self.d4, (data & 0b00000001) >>0)
        self.set_pin(self.d5, (data & 0b00000010) >>1)
        self.set_pin(self.d6, (data & 0b00000100) >>2)
        self.set_pin(self.d7, (data & 0b00001000) >>3)
        self.enable_pulse()

    def write_command(self, data):
        self.set_pin(self.rs, 0)
        self.write_byte(data)

    def write_data(self, data):
        self.set_pin(self.rs, 1)
        self.write_byte(data)
        self.set_pin(self.rs, 0)

    def reset(self):
        self.write_command(0x02)
        self.write_command(0x28)
        self.write_command(0x0C)
        self.write_command(0x06)
        self.write_command(0x80)
        self.msleep(2)

    def format_line(self, string, pos=0):
        if pos > 15 or pos + len(string) <= 0:
            return self.BLANK_LINE
        else:
            if pos >= 0:
                result = " " * pos + string
            else:
                result = string[-pos:] 
            if len(result) >= 16:
                return result[:16]
            else:
                return result + " " * (16 - len(result))
            
    def write_line(self, string, line, pos=0):
        formatted_line = self.format_line(string, pos)
        if(line == 1):
            self.write_command(0x80)
            for x in formatted_line:
                self.write_data(ord(x))
        if(line == 2):
            self.write_command(0xC0)
            for x in formatted_line:
                self.write_data(ord(x))

    def write_at(self, line, pos, string):
        pass

    def clear_screen(self):
        self.write_line(self.BLANK_LINE, 1)
        self.write_line(self.BLANK_LINE, 2)

    def backlight_on(self):
        self.set_pin(self.bl, 1)

    def backlight_off(self):
        self.set_pin(self.bl, 0)
    
    def cursor_on(self):
        self.write_command(0x0E)
   
    def cursor_off(self):
        self.write_command(0x0C)

    def cursor_blink(self):
        self.write_command(0x0D)
        
    def cleanup(self):
        GPIO.cleanup()
