import datetime
import json
import os

from backend.utils.utils import get_specyfic_time, singleton
from settings import *


@singleton
class ReportCreator():

    def _initialize(self, summary_paths):
        self.report = {}
        self.summary_paths = summary_paths
        self.start_date, self.end_date = self._get_edged_dates()

        report_name = f'ActivityReport_{self.start_date}_{self.end_date}.json'
        self.report_path = os.path.join(REPORT_DIR, report_name)

    def make_report(self, summary_path):
        self._initialize(summary_path)

        for summary_path in self.summary_paths:
            with open(summary_path, 'r') as json_file:
                summary = json.load(json_file)
                for activity in summary:
                    try:
                        self._update_activity(summary, activity)
                    except KeyError:
                        self._create_new_activity(summary, activity)
        else:
            self._add_specyfic_time()

        self._save_report()

    def delete_report(self, file):
        os.remove(file)

    def _create_new_activity(self, summary, activity):
        report, summary = {}, summary[activity]
        report['num_entries'] = summary['num_entries']
        report['max_entry'] = summary['max_entry']
        report['entries_total_time'] = {}
        report['entries_total_time']['total_time'] = summary['entries_total_time']['total_time']
        self.report[activity] = report

    def _update_activity(self, summary, activity):
        report, summary = self.report[activity], summary[activity]
        report['num_entries'] += summary['num_entries']
        if summary['max_entry']['total_time'] > report['max_entry']['total_time']:
            report['max_entry'] = summary['max_entry']
        report['entries_total_time']['total_time'] += summary['entries_total_time']['total_time']

    def _add_specyfic_time(self):
        for activity in self.report:
            total_time = self.report[activity]['entries_total_time']['total_time']
            self.report[activity]['entries_total_time'].update(
                get_specyfic_time(total_time))

    def _get_edged_dates(self):
        start_date_filename = os.path.basename(min(self.summary_paths))
        end_date_filename = os.path.basename(max(self.summary_paths))

        start_date = self._extract_date_from_file(start_date_filename)
        end_date = self._extract_date_from_file(end_date_filename)

        return start_date, end_date

    def _extract_date_from_file(self, file):
        items = file.split('.', maxsplit=1)[0]
        date = '-'.join(items.split('_')[2:])
        return date

    def _save_report(self):
        with open(self.report_path, 'w') as json_file:
            json.dump(self.report, json_file, indent=4)
