import win32gui
from pywinauto import Application


def get_active_window():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name


def get_chrome_url():
    app = Application(backend='uia')
    app.connect(title_re=".*Chrome.*", found_index=0)
    element_name="Address and search bar"
    dlg = app.top_window()
    url = dlg.child_window(title=element_name, control_type="Edit").get_value()
    return url