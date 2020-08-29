import tkinter as tk


class Message():
    @staticmethod
    def show_message(type, title, message):
        if type == 'info':
            return Message.show_info_message(title, message)
        elif type == 'warning':
            return Message.show_warning_message(title, message)
        else:
            raise KeyError('Message type is not supported')

    @staticmethod
    def show_info_message(title, message):
        tk.messagebox.showinfo(title=title, message=message)

    @staticmethod
    def show_warning_message(title, message):
        tk.messagebox.showwarning(title=title, message=message)
