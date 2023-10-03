import locale
from time import sleep
from threading import Thread
from datetime import datetime

class Displaytime(Thread):
    def __init__(self, lcd, alarm):
        self.lcd = lcd
        self.alarm = alarm
        self.current_time = None
        self.current_date = None
        self.show = True
        self.running = True
        Thread.__init__(self)

    def run(self):
        while self.running:
            if self.show:
                self.display_time()
            sleep(1)

    def stop(self):
        self.running = False

    def display_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time != self.current_time:
            self.alarm.reset()
            self.current_time = current_time
            self.lcd.write_line(current_time, 1)
            current_date = now.strftime("%a %-d %b")
            if current_date != self.current_date:
                self.current_date = current_date
                self.lcd.write_line(current_date.title(), 2)
