from backend.editors.desktop_app_parser import DesktopAppParser
from backend.editors.website_parser import WebsiteParser
from backend.utils.utils import singleton
from user_interface.report.table_creator import TableCreator


@singleton
class SummaryCreator:
    def __init__(self):
        self.table_creator = TableCreator()
        self.apps_parser = DesktopAppParser()
        self.web_parser = WebsiteParser()

    def create(self, report, frame):
        summary_report = self._adjust_summary(report)
        self.table_creator.create(summary_report, frame)

    def _adjust_summary(self, report):
        summary_report = report.copy()
        summary_report.reset_index(inplace=True)
        summary_report.rename(columns={'index': 'ID'}, inplace=True)
        summary_report.drop(
            columns=['Max Entry Total Time', 'Entries Total Time'], inplace=True)

        summary_report['Activity'] = summary_report['Activity'].apply(
            lambda x: '<UNKNOWN_APP>' if x in self.apps_parser.unknown_apps else
                      '<UNKNOWN_WEBSITE>' if x in self.web_parser.unknown_websites else x)

        return summary_report
