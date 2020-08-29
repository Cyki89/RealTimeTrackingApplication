import json
import os
import tkinter as tk

from backend.editors.report_creator import ReportCreator
from settings import *
from user_interface.message.message import Message
from user_interface.pages.template import PageTemplate
from user_interface.report.ui_report_creator import UIReportCreator


class ReportPage(PageTemplate):
    def __init__(self, controler):
        super().__init__(controler)

        self.report_creator = ReportCreator()
        self.ui_report_creator = UIReportCreator()

        command_buttons = {'Make\nReport': self.make_report,
                           'Show\nReport': self.show_report,
                           'Compare\nReports': self.compare_reports,
                           'Delete\nReport': self.delete_report}

        self.split_lower_left_frame(command_buttons)

    def make_report(self):
        report_files = self.select_files(
            files_dir=SUMMARY_DIR, title='Select the files you want to include in the report')

        if not report_files:
            Message.show_message(
                type='warning', title='Failure', message='No file has been selected')
            return

        self.report_creator.make_report(report_files)

        Message.show_message(type='info',
                             title='Success',
                             message=f'Report was successfully saved in {self.report_creator.report_path}')

    def show_report(self):
        report_file = self.select_file(
            file_dir=REPORT_DIR, title='Select report you want to show')
        if not report_file:
            Message.show_message(
                type='warning', title='Failure', message='No file has been selected')
            return

        self.ui_report_creator.create_report(file_path=report_file,
                                             summary_frame=self.top_main_frame,
                                             plot_frame=self.bottom_main_frame)

    def compare_reports(self):
        first_report_file = self.select_file(
            file_dir=REPORT_DIR, title='Select first report you want to compare')

        second_report_file = self.select_file(
            file_dir=REPORT_DIR, title='Select second report you want to compare')

        if not first_report_file or not second_report_file:
            Message.show_message(
                type='warning', title='Failure', message='First or second report file has not been selected')
            return

        self.ui_report_creator.create_report(file_path=first_report_file,
                                             summary_frame=self.top_main_frame)

        self.ui_report_creator.create_report(file_path=second_report_file,
                                             summary_frame=self.bottom_main_frame)

    def delete_report(self):
        report_file = self.select_file(
            file_dir=REPORT_DIR, title='Select report you want to delete')
        if not report_file:
            Message.show_message(
                type='warning', title='Failure', message='No file has been selected')
            return

        self.report_creator.delete_report(report_file)
        Message.show_message(type='info',
                             title='Success',
                             message=f'Report {report_file} was successfully deleted')
