import os
import tkinter as tk

from PIL import Image, ImageTk

from settings import *
from user_interface.events.events import open_tutorial
from user_interface.pages.page_registrator import PageRegistrator
from user_interface.time_tracker.ui_time_tracker import UITimeTracker


class PageTemplate(tk.Frame):
    FILE_TYPES = [('all files', '.*'), ('json files', '.json')]

    def __init__(self, controler):
        self.controler = controler
        self.page_registrator = PageRegistrator()
        self.ui_time_tracker = UITimeTracker()

        super().__init__(self.controler)

        self.split_root()
        self.split_left_frame()
        self.split_top_frame()
        self.split_upper_left_frame()

    def split_root(self):
        self.top_frame = self.create_main_frame()
        self.top_frame.place(relx=0.15, rely=0.02,
                             relwidth=0.83, relheight=0.05)

        self.top_main_frame = self.create_main_frame()
        self.top_main_frame.place(
            relx=0.15, rely=0.09, relwidth=0.83, relheight=0.435)

        self.bottom_main_frame = self.create_main_frame()
        self.bottom_main_frame.place(
            relx=0.15, rely=0.544, relwidth=0.83, relheight=0.435)

        self.left_frame = self.create_main_frame()
        self.left_frame.place(relx=0.02, rely=0.02,
                              relwidth=0.11, relheight=0.96)

    def split_left_frame(self):
        self.upper_left_frame = tk.Frame(self.left_frame, bg=FRAME_COLOR)
        self.upper_left_frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

        self.lower_left_frame = tk.Frame(self.left_frame, bg='white')
        self.lower_left_frame.place(
            relx=0, rely=0.6, relwidth=1, relheight=0.4)

    def split_top_frame(self):
        self.top_frame.grid_rowconfigure(0, weight=1)
        [self.top_frame.grid_columnconfigure(i, weight=1) for i in range(7)]

        self.logo = ImageTk.PhotoImage(Image.open(APP_LOGO_FILE))
        self.logo_label = tk.Label(self.top_frame, image=self.logo, bg='white')
        self.logo_label.grid(row=0, column=0, columnspan=3,
                             sticky='nswe', padx=0, pady=5)

        self.start_button = tk.Button(
            self.top_frame,
            text='Start Time Tracking',
            fg=BUTTON_FONT_COLOR,
            bg=BUTTON_COLOR,
            command=lambda: self.ui_time_tracker.start_time_tracking()
        )
        self.start_button.grid(
            row=0, column=4, sticky='nswe', padx=30, pady=5)

        self.stop_button = tk.Button(
            self.top_frame,
            text='Stop Time Tracking',
            fg=BUTTON_FONT_COLOR,
            bg=BUTTON_COLOR,
            command=lambda: self.ui_time_tracker.stop_time_tracking()
        )
        self.stop_button.grid(row=0, column=5, sticky='nswe', padx=0, pady=5)

        self.tutorial_button = tk.Button(
            self.top_frame,
            text='Tutorial',
            fg=BUTTON_FONT_COLOR,
            bg=BUTTON_COLOR,
            command=open_tutorial
        )
        self.tutorial_button.grid(
            row=0, column=6, sticky='nswe', padx=30, pady=5)

    def split_upper_left_frame(self):
        pages = self.page_registrator.pages

        self.upper_left_frame.grid_columnconfigure(0, weight=1)

        for i, (name, page) in enumerate(pages.items()):
            tk.Grid.rowconfigure(self.upper_left_frame, i, weight=1)

            button = tk.Button(
                self.upper_left_frame,
                text=name,
                fg=BUTTON_FONT_COLOR,
                bg=BUTTON_COLOR,
                command=self.callbackFactory(self.controler, page)
            )
            button.grid(row=i, column=0, sticky='nswe', padx=10, pady=10)

    def split_top_main_frame(self):
        self.left_top_main_frame = tk.Frame(
            self.top_main_frame, bg=FRAME_COLOR)
        self.left_top_main_frame.pack(side='left', fill='both', expand=True)

        self.right_top_main_frame = tk.Frame(
            self.top_main_frame, bg=FRAME_COLOR)
        self.right_top_main_frame.pack(side='right', fill='both', expand=True)

    def split_bottom_main_frame(self):
        self.left_bottom_main_frame = tk.Frame(
            self.bottom_main_frame, bg=FRAME_COLOR)
        self.left_bottom_main_frame.pack(side='left', fill='both', expand=True)

        self.right_bottom_main_frame = tk.Frame(
            self.bottom_main_frame, bg=FRAME_COLOR)
        self.right_bottom_main_frame.pack(
            side='right', fill='both', expand=True)

    def split_lower_left_frame(self, command_buttons):
        self.lower_left_frame.grid_columnconfigure(0, weight=1)

        for i, (name, command) in enumerate(command_buttons.items()):
            tk.Grid.rowconfigure(self.lower_left_frame, i, weight=1)
            button = tk.Button(
                self.lower_left_frame,
                text=name,
                bg=SECOND_BUTTON_COLOR,
                command=command
            )
            button.grid(row=i, column=0, sticky='we', padx=10, pady=10)

    def create_main_frame(self):
        return tk.Frame(self.controler,
                        bg=FRAME_COLOR,
                        highlightbackground=FRAME_BORDER_COLOR,
                        highlightcolor=FRAME_BORDER_COLOR,
                        highlightthickness=FRAME_BORDER_SIZE)

    def callbackFactory(self, controler, page):
        def callback():
            return controler.show_page(page(controler))
        return callback

    def select_file(self, file_dir, title):
        file = tk.filedialog.askopenfilename(parent=self,
                                             initialdir=os.path.join(
                                                 os.getcwd(), file_dir),
                                             title=title,
                                             filetypes=self.FILE_TYPES)
        return file

    def select_files(self, files_dir, title):
        files = tk.filedialog.askopenfilenames(parent=self,
                                               initialdir=os.path.join(
                                                   os.getcwd(), files_dir),
                                               title=title,
                                               filetypes=self.FILE_TYPES)
        return files
