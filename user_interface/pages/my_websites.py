import tkinter as tk

from backend.editors.website_parser import WebsiteParser
from settings import *
from user_interface.boxes.dialog_box import DialogBox
from user_interface.layout.layout_creator import LayoutCreator
from user_interface.message.message import Message
from user_interface.pages.template import PageTemplate


class MyWebsitesPage(PageTemplate):
    def __init__(self, controler):
        self.layout_creator = LayoutCreator()
        self.web_parser = WebsiteParser()

        super().__init__(controler)

        command_buttons = {'Show\nRegistered\nWebsites': self.show_registered_websites,
                           'Show\nUnknown\nWebsites': self.show_unknown_websites,
                           'Register\nNew\nWebsite': self.register_new_website,
                           'Delete\nRegistered\nWebsite': self.delete_registered_website,
                           'Delete\nUnknown\nWebsites': self.delete_all_unknows_websites}

        self.split_lower_left_frame(command_buttons)
        self.split_top_main_frame()
        self.split_bottom_main_frame()

    def show_registered_websites(self):
        left_controler = self.left_top_main_frame
        right_controler = self.right_top_main_frame
        file_path = REGISTERED_WEBSITES_FILE
        headers = ['Registered Webstite Keyword', 'Website Name']

        self.layout_creator.create(
            left_controler, right_controler, file_path, headers)

    def show_unknown_websites(self):
        left_controler = self.left_bottom_main_frame
        right_controler = self.right_bottom_main_frame
        file_path = UNKNOWN_WEBSITES_FILE
        headers = ['Unknown Website Keywords', 'Website Date Added']

        self.layout_creator.create(
            left_controler, right_controler, file_path, headers)

    def register_new_website(self):
        dialog_box = DialogBox(master=self,
                               prompt1="Website Keyword: ",
                               prompt2="Website Name: ",
                               info=("Website keyword should be a unique word by which you can identify the website\n"
                                     "* Use the option 'show_unknown_websites' and set the appropriate keyword for the website"))

        web_key, web_value = dialog_box.item_key, dialog_box.item_value
        if not web_key or not web_value:
            Message.show_message(
                type='warning', title='Failure', message='Website keyword or name has not been entered')
            return

        self.web_parser.register_website(web_key, web_value)
        Message.show_message(type='info',
                             title='Success',
                             message=f'Website {web_value} was successfully registered')

    def delete_registered_website(self):
        dialog_box = DialogBox(master=self,
                               prompt1="Website Keyword: ",
                               info=("Use the option 'show_registered_websites' and enter website keyword \n"
                                     "Restart application after removing any website(s)!!!"))

        web_key = dialog_box.item_key
        if not web_key:
            Message.show_message(
                type='warning', title='Failure', message='Website keyword has not been entered')
            return

        if self.web_parser.delete_registered_website(web_key):
            Message.show_message(type='info',
                                 title='Success',
                                 message=f'Website with keyword {web_key} was successfully deleted')
        else:
            Message.show_message(type='warning',
                                 title='Failure',
                                 message=f'Website keyword: "{web_key}" dont exist')

    def delete_all_unknows_websites(self):
        if tk.messagebox.askokcancel("Delete all unknown websites",
                                     "Do you really want to remove all unknown websites from the registry"):
            self.web_parser.delete_all_unknows_websites()

            Message.show_message(type='info',
                                 title='Success',
                                 message=f'Unknown websites was successfully deleted')
