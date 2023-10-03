from lcd16x2 import LCD16X2
from display_time import Displaytime
from ui import LEDS, Switch
from cron import WeekScheme, Cron, Crontab
from alarm import Alarm
import os
import time
import signal
import subprocess

running = True

# Clock modes definition
CLOCK = 0
ALARM = 1

# Set clock default mode
mode = CLOCK

# Initialize the display time and date strings
display_time = ''
display_date = ''

# Initialize LCD display, LEDs, switch and alarm objects
lcd = LCD16X2()
display_time = Displaytime(lcd)
display_time.start()
alarm = Alarm('mazrka01.mid')
switch = Switch(alarm.stop_midi)
switch.start()
leds = LEDS()

crontab = Crontab(alarm)
crontab.start()
ws = WeekScheme(tue=True)
ws.set_scheme(tue=True)
cron1 = Cron(21, 58, ws)
cron2 = Cron(20, 18, ws)
cron3 = Cron(20, 54, ws)
crontab.add_cron(cron1)
crontab.add_cron(cron2)
crontab.add_cron(cron3)

lcd.backlight_on()

# Set initial second watchdog
second_watchdog = 1
leds_state = False

# Main loop runs every minute
while running:
    time.sleep(60)
