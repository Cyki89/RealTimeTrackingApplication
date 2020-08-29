import tkinter as tk

from backend.utils.utils import singleton
from settings import *


@singleton
class LayoutCreator:
    def create(self, left_controler, right_controler, file_path, headers):
        self._prepare_controler(left_controler)
        self._prepare_controler(right_controler)

        self.create_headers(left_controler, right_controler, headers)

        apps = self.create_apps_list(file_path)
        self.create_body(left_controler, right_controler, apps)

    def create_headers(self, left_controler, right_controler, headers):
        for i, col in enumerate(headers):
            head_col = tk.Label(master=left_controler if i % 2 == 0 else
                                right_controler,
                                text=col,
                                bd=1,
                                relief='solid',
                                fg=TABLE_HEADERS_FONT_COLOR,
                                bg=TABLE_HEADERS_COLOR)
            head_col.grid(row=0, column=0, sticky='nswe')

    def create_apps_list(self, file_path):
        apps = []
        with open(file_path, 'r') as file:
            for line in file:
                keywords, col2 = line.strip(';\n').split(';')
                keywords = f'{", ".join(set(keywords.split()))}'
                apps.append((keywords, col2))
        return apps

    def create_body(self, left_controler, right_controler, apps):
        for i, items in enumerate(apps, 1):
            left_controler.grid_rowconfigure(i, weight=1)
            right_controler.grid_rowconfigure(i, weight=1)
            for j, item in enumerate(items):
                name_label = tk.Label(master=self._select_item([left_controler, right_controler], j),
                                      text=item,
                                      bd=1,
                                      bg=self._select_item(
                                          [TABLE_BODY_SECOND_COLOR, TABLE_BODY_FIRST_COLOR], i),
                                      relief='solid')
                name_label.grid(row=i, column=0, sticky='nswe')

    def _prepare_controler(self, controler):
        self._clean_controler(controler)
        self._initial_prepare_gird(controler)

    def _clean_controler(self, controler):
        for i, widget in enumerate(controler.winfo_children()):
            controler.grid_rowconfigure(i, weight=0)
            widget.destroy()

    def _initial_prepare_gird(self, controler):
        controler.grid_propagate(0)
        controler.grid_columnconfigure(0, weight=1)
        controler.grid_rowconfigure(0, weight=1)

    def _select_item(self, items, idx):
        return items[idx % len(items)]
