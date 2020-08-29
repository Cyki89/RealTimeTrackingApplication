import os
import tkinter as tk

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from backend.utils.utils import get_summary_path, singleton
from settings import *
from user_interface.report.image_frame import ImageFrame


@singleton
class PlotCreator:
    def create(self, report, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        self._add_bar_plot(figure=fig,
                           report=report,
                           label='All Entries',
                           col_name='Entries Total Time',
                           color=PLOT_SECOND_COLOR)
        self._add_bar_plot(figure=fig,
                           report=report,
                           label='Max Entry',
                           col_name='Max Entry Total Time',
                           color=PLOT_FIRST_COLOR)
        self._add_scatter_plot(figure=fig,
                               report=report,
                               label='Number of Entries',
                               col_name='Number of Entries',
                               color=SCATTER_COLOR)

        self._update_layout(figure=fig,
                            font_style=FONT,
                            color1=PLOT_LAYOUT_COLOR1,
                            color2=PLOT_LAYOUT_COLOR2)

        self._update_yaxes(figure=fig,
                           label='Total number of Entries',
                           secondary=False,
                           color=GRID_FIRST_COLOR)

        self._update_yaxes(figure=fig,
                           label='Total Time[min]',
                           secondary=True,
                           color=PLOT_SECOND_COLOR)

        self._render_plot(figure=fig, frame=frame)

    def _add_bar_plot(self, figure, report, label, col_name, color):
        figure.add_trace(go.Bar(name=label,
                                x=report.index,
                                y=report[col_name] / 60,
                                marker_color=color),
                         secondary_y=False)

    def _add_scatter_plot(self, figure, report, label, col_name, color):
        figure.add_trace(go.Scatter(name=label,
                                    x=report.index,
                                    y=report[col_name] / 60,
                                    marker_color=color),
                         secondary_y=True)

    def _update_layout(self, figure, font_style, color1, color2):
        figure.update_layout(font=dict(family=font_style),
                             barmode='overlay',
                             plot_bgcolor=color1,
                             paper_bgcolor=color1,
                             legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=1.02,
                                         xanchor="right",
                                         x=1,
                                         font=dict(family=font_style,
                                                   size=10,
                                                   color=color2)),
                             xaxis=dict(title_text='Activity ID',
                                        type='category',
                                        showticklabels=True,
                                        showgrid=False),
                             margin=dict(l=0,
                                         r=0,
                                         b=0,
                                         t=0,
                                         pad=5),)

    def _update_yaxes(self, figure, label, secondary, color):
        figure.update_yaxes(
            title_text=label, secondary_y=secondary, gridcolor=color)

    def _render_plot(self, figure, frame):
        figure.write_image(TEMP_PLOT)

        if os.path.exists(TEMP_PLOT):
            plot = ImageFrame(frame, TEMP_PLOT)
            plot.pack(fill=tk.BOTH, expand=tk.YES)
            os.remove(TEMP_PLOT)
