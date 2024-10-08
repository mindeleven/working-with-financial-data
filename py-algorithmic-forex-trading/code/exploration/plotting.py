# from anyio import current_default_worker_thread_limiter
import pandas as pd
import plotly.graph_objects as go
import datetime as dt

class CandlePlot:

    def __init__(self, df, candles=True):
        # working with copy of original data frame
        self.df_plot = df.copy()
        # add boolean to decide if candles or lines will be plotted
        self.candles = candles
        # create candle figure on instantiation
        self.create_candle_fig()
    
    def add_timestr(self):
        self.df_plot['sTime'] = [
            dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time
        ]

    def create_candle_fig(self):
        self.add_timestr()
        # create figure object from the plot
        self.fig = go.Figure()
        # add trace to graph object
        # if self.candles not true only lines will be plotted
        if self.candles == True:
            self.fig.add_trace(go.Candlestick(
                # setting options
                x       = self.df_plot.sTime,
                open    = self.df_plot.mid_o,
                high    = self.df_plot.mid_h,
                low     = self.df_plot.mid_l,
                close   = self.df_plot.mid_c,
                # styling the lines
                line    = dict(width=1),
                opacity = 1,
                # modifying appearance of candles
                increasing_fillcolor = "#24A06B",
                decreasing_fillcolor = "#CC2E3C",
                increasing_line_color = "#2EC886",
                decreasing_line_color = "#FF3A4C"
            ))
    
    def update_layout(self, width, height, nticks):
        self.fig.update_yaxes(
            gridcolor = "#1f292f"
        )
        self.fig.update_xaxes(
            gridcolor = "#1f292f",
            # removing range slider
            rangeslider = dict(
                visible = False
            ),
            # how many ticks do we want to see on x-axis?
            nticks = nticks
        )
        # modifying the colors
        self.fig.update_layout(
            width  = width,
            height = height,
            margin = dict(l=10, r=10, b=10, t=10),
            paper_bgcolor="#2c303c",
            plot_bgcolor="#2c303c",
            font = dict(size=8, color="#e1e1e1")
        )
    
    # line_traces are the columns that should be included
    def add_traces(self, line_traces):
        for t in line_traces:
            self.fig.add_trace(go.Scatter(
            x = self.df_plot.sTime,
            y = self.df_plot[t],
            line = dict(width = 2),
            line_shape='spline',
            name=t
        ))

    def show_plot(self, width=900, height=400, nticks=5, line_traces=[]):
        self.add_traces(line_traces)
        self.update_layout(width, height, nticks)
        self.fig.show()
