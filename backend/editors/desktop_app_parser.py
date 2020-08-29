import json
import os
import re
from datetime import datetime

from backend.editors.regex_dict import RegexDict
from backend.utils.utils import get_specyfic_time, singleton
from settings import *


@singleton
class DesktopAppParser():

    def __init__(self):
        self.unknown_apps = self._get_unknown_apps()
        self.registered_apps = self._get_registered_apps()

    def get_app(self, active_window):
        try:
            active_window = self.registered_apps[active_window]
        except KeyError:
            if active_window:
                self.add_unknown_app(active_window)
        return active_window

    def _get_registered_apps(self):
        regex_dict = RegexDict()
        if os.path.exists(REGISTERED_APPS_FILE):
            with open(REGISTERED_APPS_FILE, 'r') as file:
                for line in file:
                    key, value, _ = line.split(';')
                    regex_dict[re.compile(fr'\b{key}\b')] = value
        return regex_dict

    def _get_unknown_apps(self):
        if os.path.exists(UNKNOWN_APPS_FILE):
            unknown_apps = {}
            with open(UNKNOWN_APPS_FILE, 'r') as file:
                for line in file:
                    key, value, _ = line.split(';')
                    unknown_apps[key] = value
            return unknown_apps

    def add_unknown_app(self, app):
        if app not in self.unknown_apps:
            self.unknown_apps[app] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            self. _save_unknown_app(app)

    def _save_unknown_app(self, app):
        with open(UNKNOWN_APPS_FILE, 'a') as file:
            file.write(f'{app};{self.unknown_apps[app]};\n')

    def register_app(self, app_key, app_value):
        with open(REGISTERED_APPS_FILE, 'a') as file:
            file.write(f'{app_key};{app_value};\n')
        self.__init__()

    def delete_registered_app(self, app_key):
        is_deleted = False
        temp_file_path = os.path.join(APP_DIR, 'apps.txt')
        with open(REGISTERED_APPS_FILE, 'r') as old_file,\
                open(temp_file_path, 'w') as new_file:
            for line in old_file:
                if not line.split(';')[0].lower() == app_key.lower():
                    new_file.write(line)
                else:
                    is_deleted = True
        os.remove(REGISTERED_APPS_FILE)
        os.rename(temp_file_path, REGISTERED_APPS_FILE)
        self.__init__()
        return is_deleted

    def delete_all_unknows_apps(self):
        with open(UNKNOWN_APPS_FILE, 'w'):
            pass
        self.__init__()
