import webbrowser
from tkinter import messagebox

from backend.utils.utils import get_summary_path
from settings import *
from user_interface.report.ui_report_creator import UIReportCreator


def show_daily_report(controler):
    UIReportCreator().create_report(file_path=get_summary_path(),
                                    summary_frame=controler.top_main_frame,
                                    plot_frame=controler.bottom_main_frame)
    controler.after(30000, lambda: show_daily_report(controler))


def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()


def open_tutorial():
    webbrowser.open(url=TUTORIAL_PATH, new=1)
