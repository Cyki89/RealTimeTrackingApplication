import os
import tkinter as tk

from settings import *
from user_interface.boxes.dialog_box import DialogBox
from user_interface.layout.layout_creator import LayoutCreator
from user_interface.message.message import Message
from user_interface.pages.template import PageTemplate


class SettingsPage(PageTemplate):

    def __init__(self, controler):
        self.layout_creator = LayoutCreator()

        super().__init__(controler)

        command_buttons = {'Show\nBase Settings': self.show_settings,
                           'Show\nDirs/Files Patch': self.show_patchs,
                           'Change\nSetting': self.change_setting}

        self.split_lower_left_frame(command_buttons)
        self.split_top_main_frame()
        self.split_bottom_main_frame()

    def show_settings(self):
        left_controler = self.left_top_main_frame
        right_controler = self.right_top_main_frame
        file_path = BASE_SETTINGS_FILE
        headers = ['Setting', 'Current Value']

        self.layout_creator.create(
            left_controler, right_controler, file_path, headers)

    def show_patchs(self):
        left_controler = self.left_bottom_main_frame
        right_controler = self.right_bottom_main_frame
        file_path = PATCHS_FILE
        headers = ['Setting', 'Current Patch']

        self.layout_creator.create(
            left_controler, right_controler, file_path, headers)

    def change_setting(self):
        dialog_box = DialogBox(master=self,
                               prompt1='Setting Key: ',
                               prompt2='Setting Value: ',
                               info=('Enter setting name and value to make update\n'
                                     'Restart application after any setting(s) update!!!'))
        setting_key, setting_value = dialog_box.item_key, dialog_box.item_value

        if setting_key and setting_value:
            try:
                SETTINGS_INSTANCE.change_settings(
                    setting_key.upper(), setting_value)
                Message.show_message(
                    type='info',
                    title='Success',
                    message=f'Setting {setting_key} was successfully updated to {setting_value}')
            except KeyError as exc:
                Message.show_message(
                    type='warning', title='Failure', message=exc)
