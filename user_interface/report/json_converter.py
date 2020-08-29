import datetime
import os

import pandas as pd

from backend.utils.utils import singleton
from settings import *


@singleton
class JsonToDataFrameConverter:
    def convert(self, summary_path):
        report = self._read_json_if_exists(summary_path)
        if report.empty:
            return report

        report = self._parse_json(report)
        report = self._parse_date_columns(report)
        report = self._select_columns(report)

        self._rename_columns(report)
        self._sort_values_by_total_time(report)
        self._set_and_reset_index(report)

        return self._truncate_report(report, NUM_ACTIVITIES_TO_SHOW)

    def _read_json_if_exists(self, summary_path):
        if not os.path.exists(summary_path):
            return pd.DataFrame()
        return pd.read_json(summary_path).T

    def _parse_json(self, report):
        max_entry = self._parse_json_column(report, 'max_entry')

        entries_total_time = self._parse_json_column(
            report, 'entries_total_time')

        return pd.concat(objs=[report['num_entries'], max_entry, entries_total_time], axis=1)

    def _parse_json_column(self, report, column):
        series = report[column].apply(pd.Series)
        return pd.concat([series], axis=1, keys=[column])

    def _parse_date_columns(self, report):
        report_copy = report.copy()
        report_copy['Max Entry Start Time'] = pd.to_datetime(
            report_copy[('max_entry', 'start_time')]).dt.time
        report_copy['Max Entry End Time'] = pd.to_datetime(
            report_copy[('max_entry', 'end_time')]).dt.time

        report_copy['Max Entry Exact Time'] = report_copy[('max_entry', 'total_time')]\
            .apply(lambda x: str(datetime.timedelta(seconds=x)))
        report_copy[('Entries Exact Time')] = report_copy[('entries_total_time', 'total_time')]\
            .apply(lambda x: str(datetime.timedelta(seconds=x)))
        return report_copy

    def _select_columns(self, report):
        return report[[
            'Max Entry Start Time',
            'Max Entry End Time',
            ('max_entry', 'total_time'),
            'Max Entry Exact Time',
            'num_entries',
            ('entries_total_time', 'total_time'),
            'Entries Exact Time'
        ]]

    def _rename_columns(self, report):
        columns = ['Max Entry Start Time', 'Max Entry End Time', 'Max Entry Total Time',
                   'Max Entry Exact Time', 'Number of Entries', 'Entries Total Time', 'Entries Exact Time']
        report.columns = columns

    def _sort_values_by_total_time(self, report):
        report.sort_values(by='Entries Total Time',
                           ascending=False, inplace=True)

    def _set_and_reset_index(self, report):
        report.index.names = ['Activity']
        report.reset_index(inplace=True)

    def _truncate_report(self, report, num_activities):
        return report.iloc[:num_activities]
