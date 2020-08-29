import datetime


class Timer():
    def __init__(self):
        self.reset_timer()
        self.start()

    def start(self):
        self._start = datetime.datetime.now()

    def stop(self):
        self._stop = datetime.datetime.now()

    def get_time_interval(self):
        self.stop()
        time_interval = (self._start, self._stop)
        self.reset_timer()
        self.start()
        return time_interval

    def reset_timer(self):
        self._start = 0
        self._stop = 0
