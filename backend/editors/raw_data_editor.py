import json
import os

from backend.editors.desktop_app_parser import DesktopAppParser
from backend.editors.website_parser import WebsiteParser
from backend.utils.utils import get_specyfic_time, singleton
from settings import *


@singleton
class RawDataEditor:

    def __init__(self):
        self.apps_parser = DesktopAppParser()
        self.webs_parser = WebsiteParser()

    def delete_raw_data(self, json_file):
        self._delete_file(json_file)

        summary_name = f'Summary_{os.path.basename(json_file)}'
        summary_file = os.path.join(SUMMARY_DIR, summary_name)
        self._delete_file(summary_file)

    def _delete_file(self, file):
        if os.path.exists(file):
            os.remove(file)

    def correct_raw_data(self, json_file):
        data = self._read_json(json_file)

        self._replace_names(data)

        self._save_json(json_file, data)

        self._correct_summary(json_file, data, SUMMARY_DIR)

    def _correct_summary(self, json_file, data, SUMMARY_DIR):
        json_file = os.path.basename(json_file)

        data_merged = self._merge_activities(data)

        summary = self._summarize(data_merged)

        summary_file = os.path.join(SUMMARY_DIR, f'Summary_{json_file}')
        self._save_json(summary_file, summary)

    def _read_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        return data

    def _save_json(self, json_file, data):
        with open(f'{json_file}', 'w') as file:
            json.dump(data, file, indent=4)

    def _replace_names(self, data):
        registered_apps = self.apps_parser.registered_apps
        registered_webs = self.webs_parser.registered_websites

        for activity in data['activities']:
            try:
                activity['name'] = registered_apps[activity['name']]
            except KeyError:
                try:
                    activity['name'] = registered_webs[activity['name']]
                except KeyError:
                    pass

    def _merge_activities(self, data):
        _data = {}
        for activity in data['activities']:
            if activity['name'] in _data:
                _data[activity['name']].extend(activity['time_entries'])
            else:
                _data[activity['name']] = activity['time_entries']
        return _data

    def _summarize(self, data):
        summary = {}
        for name, time_entries in data.items():
            total_time = sum(time_entry['total_time']
                             for time_entry in time_entries)
            entries_total_time = {}
            entries_total_time['total_time'] = total_time
            entries_total_time.update(get_specyfic_time(total_time))

            max_entry = max(
                (time_entry for time_entry in time_entries),
                key=lambda x: x['total_time']
            )

            summary[name] = {
                'num_entries': len(time_entries),
                'max_entry': max_entry,
                'entries_total_time': entries_total_time
            }
        return summary
