import json
import os
import tkinter as tk

from backend.editors.raw_data_editor import RawDataEditor
from settings import *
from user_interface.message.message import Message
from user_interface.pages.template import PageTemplate
from user_interface.report.ui_report_creator import UIReportCreator


class DailySummariesPage(PageTemplate):
    def __init__(self, controler):
        super().__init__(controler)

        self.ui_report_creator = UIReportCreator()
        self.data_editor = RawDataEditor()

        command_buttons = {'Show\nDaily Summary': self.show_summary,
                           'Compare\nDaily Summaries': self.compare_summaries,
                           'Update\nRaw Data': self.update_raw_data,
                           'Delete\nRaw Data': self.delete_raw_data}

        self.split_lower_left_frame(command_buttons)

    def show_summary(self):
        summary_file = self.select_file(
            file_dir=SUMMARY_DIR, title='Select daily summary you want to show')
        if not summary_file:
            Message.show_message(
                type='warning', title='Failure', message='No file has been selected')
            return

        self.ui_report_creator.create_report(file_path=summary_file,
                                             summary_frame=self.top_main_frame,
                                             plot_frame=self.bottom_main_frame)

    def compare_summaries(self):
        first_summary_file = self.select_file(
            file_dir=SUMMARY_DIR, title='Select first daily summary you want to compare')

        second_summary_file = self.select_file(
            file_dir=SUMMARY_DIR, title='Select second daily summary you want to compare')

        if not first_summary_file or not second_summary_file:
            Message.show_message(
                type='warning', title='Failure', message='First or second summary file has not been selected')
            return

        self.ui_report_creator.create_report(file_path=first_summary_file,
                                             summary_frame=self.top_main_frame)

        self.ui_report_creator.create_report(file_path=second_summary_file,
                                             summary_frame=self.bottom_main_frame)

    def update_raw_data(self):
        Message.show_message(
            type='info',
            title='Info',
            message='This feature update app name in raw json file and coresponding daily summary'
        )

        json_file = self.select_file(
            file_dir=JSON_DIR, title='Select file you want to update')
        if not json_file:
            Message.show_message(
                type='warning', title='Failure', message='No file has been selected')
            return

        self.data_editor.correct_raw_data(json_file)

        json_name = os.path.basename(json_file)
        summary_name = f'Summary_{json_name}'

        Message.show_message(
            type='info',
            title='Success',
            message=(f'Json File: {json_name} and\n'
                     f'Daily Summary: {summary_name} were successfully updated')
        )

    def delete_raw_data(self):
        Message.show_message(
            type='info',
            title='Info',
            message='This feature delete raw json file and coresponding daily summary'
        )

        json_file = self.select_file(
            file_dir=JSON_DIR, title='Select file you want to delete')
        if not json_file:
            Message.show_message(
                type='warning', title='Failure', message='No file has been selected')
            return

        self.data_editor.delete_raw_data(json_file)

        json_name = os.path.basename(json_file)
        summary_name = f'Summary_{json_name}'

        Message.show_message(
            type='info',
            title='Success',
            message=(f'Json File: {json_name} and\n'
                     f'Daily Summary: {summary_name} were successfully deleted')
        )
