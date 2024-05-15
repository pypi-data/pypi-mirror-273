from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from ketacli.sdk.output.format import OutputTable
from ketacli.sdk.chart import utils


class SingleValueChart:
    def __init__(self, data: OutputTable, single_field, title=None, extra_fields: list = None, **kwargs):
        self.data = data
        self.single_field = single_field
        self.title = title
        self.extra_fields = extra_fields
        self.kwargs = kwargs
        self.border_style = ""
        self.subtitle = kwargs.pop("subtitle", "")
        self.child = kwargs.pop("child", {})

    def __rich_console__(self, console, options):
        width = options.max_width or console.width
        self.height = options.height or console.height
        prefix = self.kwargs.get("prefix", "")
        suffix = self.kwargs.get("suffix", "")
        style = self.kwargs.get("style", "")
        threshold = self.kwargs.get("threshold", {})
        _format = self.kwargs.get("format", None)

        index = self.data.header.index(self.single_field)
        single_value = utils.format([str(x[index]) for x in self.data.rows][0], type=_format)
        if threshold:
            style = utils.threshold(single_value, **threshold)
        single_value = f"{prefix}{single_value}{suffix}"
        extra_values = []
        if self.extra_fields:
            for extra_field in self.extra_fields:
                extra_values.append(
                    f"{extra_field}: {[str(x[self.data.header.index(extra_field)]) for x in self.data.rows][0]}")
        extra_value = "\n".join(extra_values)
        padding = ((int(self.height) - (len(self.extra_fields) + 3)) // 2, 0)
        texts = ((single_value, style), "\n", extra_value)
        panel = Panel(Text.assemble(*texts, justify="center"),
                      expand=True, padding=padding, title=self.title, width=width, height=self.height,
                      border_style=self.border_style, subtitle=Text(self.subtitle, justify="center", style="#808080"), )

        yield panel


if __name__ == '__main__':
    console = Console()
    table = OutputTable(["main", "res", "shard", "pc"], [[1, 2, 3, 100]])
    console.print(SingleValueChart(table, "pc", title="title", extra_fields=["main", "res", "shard"]))
