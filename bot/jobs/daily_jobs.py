import datetime
import pytz
from telegram.ext import JobQueue

from bot.handlers.daily import DailyHanlder


class DailyJobsManager:
    def __init__(self, job_que: JobQueue, daily_handler: DailyHanlder) -> None:
        self.job_que = job_que
        self.daily_hanlder = daily_handler
        self.tehran_tz = pytz.timezone("Asia/Tehran")
        self.tehran_time_2am = datetime.time(hour=2, minute=0, tzinfo=self.tehran_tz)

    def schedule_open_group(self, hours: int = 8, minitue: int = 0):
        tehran_time = datetime.time(hour=hours, minute=minitue, tzinfo=self.tehran_tz)

        self.job_que.run_daily(self.daily_hanlder.open_group, time=tehran_time)

    def schedule_close_group(self, hours: int = 2, minute: int = 0):
        tehran_time = datetime.time(hour=hours, minute=minute, tzinfo=self.tehran_tz)

        self.job_que.run_daily(self.daily_hanlder.close_group, time=tehran_time)
