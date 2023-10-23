class WeekScheme:
    def __init__(self, sun=False, mon=False, tue=False, wed=False, thu=False, fri=False, sat=False):
        self.set_scheme(sun, mon, tue, wed, thu, fri, sat)

    def set_scheme(self, sun=False, mon=False, tue=False, wed=False, thu=False, fri=False, sat=False):
        self.week = [sun, mon, tue, wed, thu, fri, sat]

    def is_day_active(self, now):
        return self.week[int(now.strftime('%w'))]

class Cron:
    def __init__(self, hour, minute, week_scheme):
        self.set_cron(hour, minute, week_scheme)

    def set_cron(self, hour, minute, week_scheme):
        self.hour = hour
        self.minute = minute
        p_hour = '0{}'.format(hour) if hour < 10 else hour
        p_minute = '0{}'.format(minute) if minute < 10 else minute
        self.time = '{}:{}'.format(hour, minute)
        self.week_scheme = week_scheme

    def matches_now(self, now):
        if self.week_scheme.is_day_active(now) and self.time == now.strftime("%H:%M"):
            return True
        else:
            return False

class Crontab():
    def __init__(self, callback=None):
        self.callback = callback
        self.crontab = []

    def add_cron(self, cron):
        self.crontab.append(cron)

    def del_cron(self, index):
        self.crontab.pop(index)

    def is_triggering(self, now):
        for cron in self.crontab:
            if cron.matches_now(now):
               return True
        return False
