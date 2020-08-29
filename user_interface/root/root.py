import tkinter as tk

from settings import *
from user_interface.events.events import on_closing
from backend.utils.utils import singleton


@singleton
class Root(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Time Tracking Aplication')
        self.protocol("WM_DELETE_WINDOW", lambda: on_closing(self))
        self.configure(background=BACKGROUND_COLOR,
                       height=APP_HEIGHT, width=APP_WIDTH)

    def show_page(self, page):
        page.tkraise()
