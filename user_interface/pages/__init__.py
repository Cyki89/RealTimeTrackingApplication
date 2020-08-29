from user_interface.pages.my_apps import MyAppsPage
from user_interface.pages.page_registrator import PageRegistrator
from user_interface.pages.report import ReportPage
from user_interface.pages.settings import SettingsPage
from user_interface.pages.time_tracking import TimeTrackingPage
from user_interface.pages.daily_summaries import DailySummariesPage
from user_interface.pages.my_websites import MyWebsitesPage

pages_to_register = [TimeTrackingPage, MyAppsPage, MyWebsitesPage,
                     DailySummariesPage, ReportPage, SettingsPage]

page_registrator = PageRegistrator()

for page in pages_to_register:
    page_registrator.register(page.__name__, page)
