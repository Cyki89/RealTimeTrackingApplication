import tkinter as tk

from backend.utils.utils import singleton
from settings import *


@ singleton
class TableCreator:
    def create(self, summary_report, frame):
        self._prepare_frame(frame)

        self._create_headers(summary_report, frame)
        self._create_body(summary_report, frame)

    def _create_headers(self, summary_report, frame):
        frame.grid_rowconfigure(0, weight=1)
        for i, col in enumerate(summary_report.columns):
            frame.grid_columnconfigure(i, weight=1)
            head_col = tk.Label(frame,
                                text=col,
                                bd=1,
                                relief='solid',
                                fg=TABLE_HEADERS_FONT_COLOR,
                                bg=TABLE_HEADERS_COLOR)
            head_col.grid(row=0, column=i, sticky='nswe')

    def _create_body(self, summary_report, frame):
        for i, idx in enumerate(summary_report.index, 1):
            frame.grid_rowconfigure(i, weight=1)
            for j, col in enumerate(summary_report.loc[idx]):
                record = tk.Label(frame,
                                  text=str(col),
                                  bd=1,
                                  bg=TABLE_BODY_FIRST_COLOR if i % 2 == 1
                                  else TABLE_BODY_SECOND_COLOR,
                                  relief='solid')
                record.grid(row=i, column=j, sticky='nswe')

    def _prepare_frame(self, frame):
        self._clean_frame(frame)
        self._initial_prepare_gird(frame)

    def _clean_frame(self, frame):
        for i, widget in enumerate(frame.winfo_children()):
            frame.grid_rowconfigure(i, weight=0)
            widget.destroy()

    def _initial_prepare_gird(self, frame):
        frame.grid_propagate(0)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
