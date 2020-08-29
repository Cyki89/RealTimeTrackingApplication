import datetime
import os
import re
import sys
import threading
import traceback
from functools import wraps

from backend.time_tracking.restart_tracking import RestartTimeTrackingError
from settings import *


def get_specyfic_time(total_time):
    return {
        'days': total_time // 86400,
        'hours': (total_time % 86400) // 3600,
        'minutes': (total_time % 3600) // 60,
        'seconds': total_time % 60
    }


def get_jason_name():
    return f'Acivities_{datetime.datetime.now().strftime("%Y_%m_%d")}.json'


def get_json_path():
    return os.path.join(JSON_DIR, get_jason_name())


def get_summary_path():
    return os.path.join(SUMMARY_DIR, f'Summary_{get_jason_name()}')


def convert_url(url):
    return 'www.' + split_url(url)


def split_url(url):
    return url.split("/")[0]


def split_window_name(window_name):
    return window_name.split()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def restart_time_tracking():
    raise RestartTimeTracking("RESTART TIME TRACKING")


def save_data(self):
    self.add_activity()
    self.activities.save_data_to_json()
    self.activities.save_summary_to_json()


def restore_time_tracking(self):
    save_data(self)
    self.schedule.clear('daily-task')
    self.time_tracking()


def log_error(exc):
    tb = ''.join(traceback.format_exception(None, exc, exc.__traceback__))
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as file:
        file.write(f'Time: {time}\t Type: {type(exc)}\t {tb}')
        file.write('-' * 110 + '\n')


def exit_script():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def error_handling(func):

    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except RestartTimeTrackingError:
            restore_time_tracking(self)
        except KeyboardInterrupt:
            save_data(self)
        except Exception as exc:
            log_error(exc)
            restore_time_tracking(self)

    return wrapper


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
