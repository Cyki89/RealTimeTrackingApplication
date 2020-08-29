import time

import schedule

from backend.editors.desktop_app_parser import DesktopAppParser
from backend.editors.website_parser import WebsiteParser
from backend.time_tracking.activity import Activity
from backend.time_tracking.activity_list import ActivityList
from backend.time_tracking.automation_task import (get_active_window,
                                                   get_chrome_url)
from backend.time_tracking.time_entry import TimeEntry
from backend.time_tracking.timer import Timer
from backend.utils.utils import (convert_url, error_handling, get_json_path,
                                 restart_time_tracking, run_threaded,
                                 singleton, split_window_name)


@singleton
class AutoTimeTracker():
    def __init__(self, app_parser, web_parser, activities=None, real_time_report=None, timer=None, time_sleep=10):
        self.app_parser = app_parser
        self.web_parser = web_parser
        self.activities = activities
        self.real_time_report = real_time_report
        self.timer = timer
        self.time_sleep = time_sleep
        self.schedule = schedule
        self.active_window = ''
        self.last_active_window = ''

        self._running = True

    def add_activity(self):
        start, stop = self.timer.get_time_interval()
        time_entry = TimeEntry(start, stop)

        if self.last_active_window != '':
            try:
                self.activities[self.last_active_window].add_time_entry(
                    time_entry)
            except KeyError:
                self.activities[self.last_active_window] = Activity(
                    self.last_active_window)
                self.activities[self.last_active_window].add_time_entry(
                    time_entry)

        self.last_active_window = self.active_window

    def create_scheduled_tasks(self):
        self.schedule.every().day.at('00:00').do(
            restart_time_tracking).tag('daily-task')
        self.schedule.every(2).minutes.do(
            self.activities.save_data_to_json).tag('daily-task')
        self.schedule.every(2).minutes.do(
            self.activities.save_summary_to_json).tag('daily-task')

    def pre_time_tracking(self):
        json_path = get_json_path()

        self.activities = ActivityList()
        self.activities.read_data_from_json()

        self.timer = Timer()

    @error_handling
    def time_tracking(self):
        self.pre_time_tracking()
        self.create_scheduled_tasks()

        while self._running:
            self.active_window = get_active_window()

            if 'Google Chrome' in self.active_window:
                url = get_chrome_url()
                self.active_window = convert_url(url) \
                    if len(self.active_window) < 25 \
                    else self.web_parser.get_website(self.active_window)

            else:
                self.active_window = self.app_parser.get_app(
                    self.active_window)

            if self.last_active_window != self.active_window:
                self.add_activity()

            self.schedule.run_pending()

            time.sleep(self.time_sleep)
        else:
            raise KeyboardInterrupt
