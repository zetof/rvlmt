from time import sleep
from threading import Thread
from datetime import datetime
from lcd16x2 import LCD16X2
from ui import LEDS, Switch
from cron import WeekScheme, Cron, Crontab
from alarm import Alarm

class Clock(Thread):
    def __init__(self):
        self.running = True
        self.seconds = ''
        self.current_time = ''
        self.show_time = True
        self.backlight_timer = -1
        self.lcd = LCD16X2()
        self.backlight_on()
        self.alarm = Alarm()
        self.switch = Switch(self.backlight_on)
        self.leds = LEDS()
        ws = WeekScheme(mon=True)
        cron = Cron(20, 58, ws)
        self.crontab = Crontab()
        self.crontab.add_cron(cron)
        Thread.__init__(self)

    def run(self):
        while self.running:
            now = datetime.now()
            seconds = now.strftime("%S")
            self.switch.check_callback()
            self.check_backlight()
            if seconds != self.seconds:
                display_time = self.get_display_time(now)
                if display_time:
                    self.lcd.write_line(display_time['time'], 1)
                    self.lcd.write_line(display_time['date'], 2)
                    if self.crontab.is_triggering(now):
                        self.alarm.set_midi_file('mazrka01.mid ')
                        self.alarm.play_midi()
                self.seconds = seconds
            sleep(.1)

    def stop(self):
        self.running = False

    def backlight_on(self, seconds=5, timed=True):
        if self.backlight_timer == -1:
            if timed:
                self.backlight_timer = 10 * seconds
            else:
                self.backlight_timer = -1
        self.lcd.backlight_on()

    def backlight_off(self):
        self.backlight_timer = -1
        self.lcd.backlight_off()

    def check_backlight(self):
        if self.backlight_timer >= 0:
            self.backlight_timer -= 1
        if self.backlight_timer == 0:
            self.lcd.backlight_off()

    def get_display_time(self, now):
        current_time = now.strftime('%H:%M')
        if current_time != self.current_time:
            self.current_time = current_time
            if self.show_time:
                return {'time': current_time, 'date': now.strftime('%a %-d %b')}
            else:
                return None
        else:
            return None
