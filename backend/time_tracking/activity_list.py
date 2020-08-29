import json
import os

from dateutil import parser

from backend.time_tracking.activity import Activity
from backend.time_tracking.time_entry import TimeEntry
from backend.utils.utils import (get_json_path, get_specyfic_time,
                                 get_summary_path)


class ActivityList():
    def __init__(self):
        self.activities = {}
        self.json_path = get_json_path()
        self.summary_path = get_summary_path()

    def __getitem__(self, activity_name):
        return self.activities[activity_name]

    def __setitem__(self, activity_name, activity):
        self.activities[activity_name] = activity

    def read_data_from_json(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as json_file:
                data = json.load(json_file)
            for activity in data['activities']:
                self.activities[activity['name']] = Activity(activity['name'])
                for time_entry in activity['time_entries']:
                    self.activities[activity['name']].add_time_entry(
                        self.deserialize_time_entry(time_entry))

    def summarize(self):
        summary = {}
        for name, activity in self.activities.items():

            total_time = sum(
                time_entry.total_time for time_entry in activity.time_entries)
            entries_total_time = {}
            entries_total_time['total_time'] = total_time
            entries_total_time.update(get_specyfic_time(total_time))

            max_entry = max(
                (time_entry for time_entry in activity.time_entries), key=lambda x: x.total_time)

            summary[name] = {
                'num_entries': len(activity.time_entries),
                'max_entry': max_entry.serialize(),
                'entries_total_time': entries_total_time
            }

        return summary

    def save_data_to_json(self):
        with open(self.json_path, 'w') as json_file:
            json.dump(self.serialize(), json_file, indent=4)

    def save_summary_to_json(self):
        with open(self.summary_path, 'w') as json_file:
            json.dump(self.summarize(), json_file, indent=4)

    def serialize(self):
        return {
            'activities': [activity.serialize() for activity in self.activities.values()]
        }

    def deserialize_time_entry(self, time_entry):
        return TimeEntry(
            start_time=parser.parse(time_entry['start_time']),
            end_time=parser.parse(time_entry['end_time']),
        )
