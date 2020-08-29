from backend.utils.utils import singleton


@singleton
class PageRegistrator:

    def __init__(self):
        self.pages = {}

    def register(self, name, cls):
        # remove 'Page' from class name
        self.pages[name[:-4]] = cls
