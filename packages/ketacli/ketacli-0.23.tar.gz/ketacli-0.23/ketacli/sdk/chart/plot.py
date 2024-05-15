import time

import plotext as plt
from datetime import datetime
from ketacli.sdk.output.format import OutputTable


class Plot:
    def __init__(self, field_x: str, field_y: list, data: OutputTable,
                 time_format="%Y-%m-%d %H:%M:%S", title="Plot with Time on X-axis",
                 x_label="", y_label="", field_group="", plot_type="line", marker="hd", theme="dark", **kwargs):
        if isinstance(field_y, str):
            field_y = [field_y]
        self.plot_type = plot_type
        self.data = data
        self.field_x_index = 0
        self.field_y_index = []
        if field_x in data.header:
            self.field_x_index = data.header.index(field_x)

        for y in field_y:
            if y in data.header:
                self.field_y_index.append(data.header.index(y))

        self.field_x = field_x
        self.field_y = field_y
        self.time_format = time_format
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.field_group = field_group
        self.marker = marker
        self.kwargs = kwargs
        self.theme = theme
        self.child = kwargs.pop("child", {})
        self.format = kwargs.pop("format", "")
        self.subtitle = kwargs.pop("subtitle", "")

        # 设置标题和坐标轴标签

    def build(self, width, height):
        plt.clf()

        plt.title(self.title)
        plt.ylabel(self.field_y[0])
        plt.xlabel(self.field_x)

        # 绘制图形
        if self.field_group and self.field_group in self.data.header:
            field_group_index = self.data.header.index(self.field_group)
            group_names = tuple(set([x[field_group_index] for x in self.data.rows]))
            for group_name in group_names:
                if self.data.header[self.field_x_index] == "_time":
                    plt.date_form(self.time_format.replace("%", ""))
                    x = [datetime.utcfromtimestamp(x[self.field_x_index] / 1000).strftime(self.time_format) for x in
                         self.data.rows if x[field_group_index] == group_name]
                else:
                    x = [x[self.field_x_index] for x in self.data.rows if x[field_group_index] == group_name]

                ydata = []
                for y in self.field_y_index:
                    ydata.append([x[y] if x[y] is not None else 0 for x in self.data.rows if x[field_group_index] == group_name])
                for y in ydata:
                    if self.plot_type == "line":
                        if self.data.header[self.field_x_index] == "_time":
                            plt.plot(x, y, label=group_name, marker=self.marker, **self.kwargs)
                        else:
                            plt.plot(y, label=group_name, marker=self.marker, **self.kwargs)
                    elif self.plot_type == "bar":
                        plt.bar(x, y, label=group_name, marker=self.marker, **self.kwargs)
                    elif self.plot_type == "scatter":
                        plt.scatter(x, y, label=group_name, marker=self.marker, **self.kwargs)

        else:
            if self.data.header[self.field_x_index] == "_time":
                plt.date_form(self.time_format.replace("%", ""))
                x = [datetime.utcfromtimestamp(x[self.field_x_index] / 1000).strftime(self.time_format) for x in
                     self.data.rows]
            else:
                x = [x[self.field_x_index] for x in self.data.rows]
            ydata = []
            for y in self.field_y_index:
                ydata.append([x[y] if x[y] is not None else 0 for x in self.data.rows])
            for i in range(len(ydata)):
                y = ydata[i]
                if self.plot_type == "line":
                    if self.data.header[self.field_x_index] == "_time":
                        plt.plot(x, y, marker=self.marker, label=self.field_y[i], **self.kwargs)
                    else:
                        plt.plot(y, marker=self.marker, label=self.field_y[i], **self.kwargs)
                elif self.plot_type == "bar":
                    plt.bar(x, y, marker=self.marker, label=self.field_y[i], **self.kwargs)
                elif self.plot_type == "scatter":
                    plt.scatter(x, y, marker=self.marker, label=self.field_y[i], **self.kwargs)
        plt.grid(0, 1)  # 添加垂直网格线
        plt.plotsize(width, height)
        plt.theme(self.theme)
        return plt.build()

    def show(self):
        print(self.build(100, 100))


if __name__ == '__main__':
    table = OutputTable(["time", "value"], [[time.time() * 1000, 1], [time.time() * 1000, 2]])
    line_chart = Plot("time", "value", table, time_format="%Y-%m-%d %H:%M:%S",
                      title="Plot with Time on X-axis", )
    line_chart.show()
