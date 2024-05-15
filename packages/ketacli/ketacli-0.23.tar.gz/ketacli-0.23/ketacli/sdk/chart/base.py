from rich.jupyter import JupyterMixin
from rich.ansi import AnsiDecoder
from rich.console import Group


class PlotextMixin(JupyterMixin):
    def __init__(self, phase=0, title="", make_plot=None):
        self.decoder = AnsiDecoder()
        self.phase = phase
        self.title = title
        self.make_plot = make_plot

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = self.make_plot(self.width, self.height)
        self.rich_canvas = Group(*self.decoder.decode(canvas))
        yield self.rich_canvas
