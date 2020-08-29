from backend.utils.utils import singleton
from user_interface.report.json_converter import JsonToDataFrameConverter
from user_interface.report.plot_creator import PlotCreator
from user_interface.report.summary_creator import SummaryCreator


@singleton
class UIReportCreator:
    def __init__(self):
        self.json_converter = JsonToDataFrameConverter()
        self.summary_creator = SummaryCreator()
        self.plot_creator = PlotCreator()

    def create_report(self, file_path, summary_frame, plot_frame=None):
        report = self.json_converter.convert(file_path)
        if report.empty:
            return

        if plot_frame != None:
            self.plot_creator.create(report, plot_frame)

        self.summary_creator.create(report, summary_frame)
