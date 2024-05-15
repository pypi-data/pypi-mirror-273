from rich.console import Console
from ketacli.sdk.output.format import OutputTable
from rich.table import Table
from rich.panel import Panel
from rich.console import Text
from ketacli.sdk.chart import utils


class KTable:
    def __init__(self, data: OutputTable, title=None, **kwargs):
        self.data = data
        self.title = title
        self.kwargs = kwargs
        self.border_style = ""
        self.subtitle = kwargs.pop("subtitle", "")
        self.child = kwargs.pop("child", {})

    def __rich_console__(self, console, options):
        width = options.max_width or console.width
        self.height = options.height or console.height
        table = Table(show_header=True, header_style="bold magenta", width=width, expand=True, padding=0,
                      show_lines=True)

        table_data = utils.sort_values_by_header(self.data.header, self.data.rows, self.kwargs)
        table_texts = []

        for key, value in table_data.items():
            col_data = table_data[key]
            column_attributes = col_data['attributes']
            style = column_attributes.get("style", "")
            threshold = column_attributes.get("threshold", None)
            _format = column_attributes.get("format", None)
            suffix = column_attributes.get("suffix", "")
            prefix = column_attributes.get("prefix", "")
            justify = column_attributes.get("justify", "center")
            enum = column_attributes.get("enum", None)

            title = col_data['attributes'].get('alias', key)
            if not col_data['attributes'].get('is_show', True):
                continue
            table.add_column(title, style="blink", justify="center")
            row_texts = []
            for data in col_data['data']:
                if threshold:
                    style = utils.threshold(data, **threshold)
                if _format:
                    data = utils.format(data, type=_format)
                if enum:
                    enum_values = utils.enum(data, **enum)
                    data = enum_values.get("alias", data)
                    style = enum_values.get("style", style)

                text = ((f"{prefix}{data}{suffix}", style),)
                text = Text.assemble(*text, justify=justify)
                row_texts.append(text)
            table_texts.append(row_texts)

        for row_texts in [x for x in zip(*table_texts)]:
            table.add_row(*row_texts)
        title_text = Text(f"{self.title}({len(self.data.rows)})", justify="center", style="bold")
        panel = Panel(table, expand=True, padding=0, title=title_text, height=self.height,
                      border_style=self.border_style, subtitle=Text(self.subtitle, justify="center", style="#808080"),)
        yield panel


if __name__ == '__main__':
    console = Console()
    table = OutputTable(["main", "res", "shard", "pc"], [[1, 2, 3, 100]])
    console.print(KTable(table, title="title", **{
        "main": {"title": "主", "style": "bold red", "threshold": {"green": [0, 80], "red": [80, 100]}},
        "res": {"title": "资源", "style": "bold green"},
        "shard": {"title": "分片", "style": "bold blue"},
        "pc": {"title": "使用率", "style": "bold yellow"}}))
