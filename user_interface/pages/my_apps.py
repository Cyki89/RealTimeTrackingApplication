import tkinter as tk

from backend.editors.desktop_app_parser import DesktopAppParser
from settings import *
from user_interface.boxes.dialog_box import DialogBox
from user_interface.layout.layout_creator import LayoutCreator
from user_interface.message.message import Message
from user_interface.pages.template import PageTemplate


class MyAppsPage(PageTemplate):
    def __init__(self, controler):
        self.layout_creator = LayoutCreator()
        self.app_parser = DesktopAppParser()

        super().__init__(controler)

        command_buttons = {'Show\nRegistered Apps': self.show_registered_apps,
                           'Show\nUnknown Apps': self.show_unknown_apps,
                           'Register\nNew App': self.register_new_app,
                           'Delete\nRegistered App': self.delete_registered_app,
                           'Delete\nUnknown Apps': self.delete_all_unknows_apps}

        self.split_lower_left_frame(command_buttons)
        self.split_top_main_frame()
        self.split_bottom_main_frame()

    def show_registered_apps(self):
        left_controler = self.left_top_main_frame
        right_controler = self.right_top_main_frame
        file_path = REGISTERED_APPS_FILE
        headers = ['Registered Application Keyword', 'Application Name']

        self.layout_creator.create(
            left_controler, right_controler, file_path, headers)

    def show_unknown_apps(self):
        left_controler = self.left_bottom_main_frame
        right_controler = self.right_bottom_main_frame
        file_path = UNKNOWN_APPS_FILE
        headers = ['Unknown Application Keywords', 'Application Date Added']

        self.layout_creator.create(
            left_controler, right_controler, file_path, headers)

    def register_new_app(self):
        dialog_box = DialogBox(master=self,
                               prompt1="Application Keyword: ",
                               prompt2="Application Name: ",
                               info=("Application keyword should be a unique word by which you can identify the application\n"
                                     "* Use the option 'show_unknown_apps' and set the appropriate keyword for the app"))

        app_key, app_value = dialog_box.item_key, dialog_box.item_value
        if not app_key or not app_value:
            Message.show_message(
                type='warning', title='Failure', message='Application keyword or name has not been entered')
            return

        self.app_parser.register_app(app_key, app_value)
        Message.show_message(type='info',
                             title='Success',
                             message=f'Application {app_value} was successfully registered')

    def delete_registered_app(self):
        dialog_box = DialogBox(master=self,
                               prompt1="Application Keyword: ",
                               info=("Use the option 'show_registered_apps' and enter app keyword \n"
                                     "Restart application after removing any app(s)!!!"))

        app_key = dialog_box.item_key
        if not app_key:
            Message.show_message(
                type='warning', title='Failure', message='Application keyword has not been entered')
            return

        if self.app_parser.delete_registered_app(app_key):
            Message.show_message(type='info',
                                 title='Success',
                                 message=f'Application with keyword "{app_key}" was successfully deleted')
        else:
            Message.show_message(type='warning',
                                 title='Failure',
                                 message=f'Application keyword: "{app_key}" dont exist')

    def delete_all_unknows_apps(self):
        if tk.messagebox.askokcancel("Delete all unknown apps",
                                     "Do you really want to remove all unknown apps from the registry"):
            self.app_parser.delete_all_unknows_apps()

            Message.show_message(type='info',
                                 title='Success',
                                 message=f'Unknown applications was successfully deleted')
