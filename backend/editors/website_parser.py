import json
import os
import re
from datetime import datetime

from backend.editors.regex_dict import RegexDict
from backend.utils.utils import get_specyfic_time, singleton
from settings import *


@singleton
class WebsiteParser():

    def __init__(self):
        self.unknown_websites = self._get_unknown_websites()
        self.registered_websites = self._get_registered_websites()

    def get_website(self, active_window):
        try:
            active_window = self.registered_websites[active_window]
        except KeyError:
            if active_window:
                self.add_unknown_website(active_window)
        return active_window

    def _get_registered_websites(self):
        regex_dict = RegexDict()
        if os.path.exists(REGISTERED_WEBSITES_FILE):
            with open(REGISTERED_WEBSITES_FILE, 'r') as file:
                for line in file:
                    key, value, _ = line.split(';')
                    regex_dict[re.compile(fr'\b{key}\b')] = value
        return regex_dict

    def _get_unknown_websites(self):
        if os.path.exists(UNKNOWN_WEBSITES_FILE):
            unknown_websites = {}
            with open(UNKNOWN_WEBSITES_FILE, 'r') as file:
                for line in file:
                    key, value, _ = line.split(';')
                    unknown_websites[key] = value
            return unknown_websites

    def add_unknown_website(self, website):
        if website not in self.unknown_websites:
            self.unknown_websites[website] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            self. _save_unknown_website(website)

    def _save_unknown_website(self, website):
        with open(UNKNOWN_WEBSITES_FILE, 'a') as file:
            file.write(f'{website};{self.unknown_websites[website]};\n')

    def register_website(self, website_key, website_value):
        with open(REGISTERED_WEBSITES_FILE, 'a') as file:
            file.write(f'{website_key};{website_value};\n')
        self.__init__()

    def delete_registered_website(self, website_key):
        is_deleted = False
        temp_file_path = os.path.join(WEB_DIR, 'webs.txt')
        with open(REGISTERED_WEBSITES_FILE, 'r') as old_file,\
                open(temp_file_path, 'w') as new_file:
            for line in old_file:
                if not line.split(';')[0].lower() == website_key.lower():
                    new_file.write(line)
                else:
                    is_deleted = True
        os.remove(REGISTERED_WEBSITES_FILE)
        os.rename(temp_file_path, REGISTERED_WEBSITES_FILE)
        self.__init__()
        return is_deleted

    def delete_all_unknows_websites(self):
        with open(UNKNOWN_WEBSITES_FILE, 'w'):
            pass
        self.__init__()
