from user_interface.root.root import Root
from user_interface.pages.time_tracking import TimeTrackingPage

import warnings
warnings.filterwarnings('ignore')

if __name__ == '__main__':

    root = Root()
    root.show_page(TimeTrackingPage(root))
    root.mainloop()
