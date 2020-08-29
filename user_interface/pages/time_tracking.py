import threading

from settings import *
from user_interface.events.events import show_daily_report
from user_interface.pages.template import PageTemplate


class TimeTrackingPage(PageTemplate):
    def __init__(self, controler):
        super().__init__(controler)

        self.show_live_report()

    def show_live_report(self):
        report_thread = threading.Thread(
            name='report',
            target=lambda: show_daily_report(self)
        )
        report_thread.demon = True
        report_thread.start()
