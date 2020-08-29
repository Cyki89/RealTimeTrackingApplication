from backend.utils.utils import get_specyfic_time


class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = (end_time - start_time).seconds
        self.days, self.hours, self.minutes, self.seconds = get_specyfic_time(
            self.total_time).values()

    def serialize(self):
        return {
            'total_time': self.total_time,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }
