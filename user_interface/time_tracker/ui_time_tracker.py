import threading

from backend.editors.desktop_app_parser import DesktopAppParser
from backend.editors.website_parser import WebsiteParser
from backend.time_tracking.auto_time_tracker import AutoTimeTracker
from backend.utils.utils import singleton


@singleton
class UITimeTracker():
    def __init__(self):
        self.time_tracker = AutoTimeTracker(
            DesktopAppParser(), WebsiteParser())
        self.create_new_thread()

    def start_time_tracking(self):
        self.time_tracker._running = True
        self._thread.start()

    def stop_time_tracking(self):
        self.time_tracker._running = False
        self.create_new_thread()

    def create_new_thread(self):
        self._thread = threading.Thread(target=self.time_tracker.time_tracking)
        self._thread.deamon = True
