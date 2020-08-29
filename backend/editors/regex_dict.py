import re

from backend.utils.utils import singleton


class RegexDict(dict):

    def __init__(self):
        super().__init__()

    def __getitem__(self, item):
        for k, v in self.items():
            if re.search(k, item):
                return v
        raise KeyError
