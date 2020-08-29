class RestartTimeTrackingError(Exception):
    def __init__(self, warning):
        self.warning = warning

    def __str__(self):
        return f'{self.__class__.__name__} --> {self.warning}'
