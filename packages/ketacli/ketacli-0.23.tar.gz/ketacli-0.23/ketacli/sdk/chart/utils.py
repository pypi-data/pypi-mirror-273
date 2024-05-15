from datetime import datetime


def threshold(value: (float, int), **kwargs):
    """
    判断值是否在阈值范围内，返回对应的 key
    threshold = threshold(value, green=(0, 80), red=(80, 100))

    Args:
        value:
        **kwargs:

    Returns:

    """
    if not kwargs:
        return ""
    if not isinstance(value, (float, int)):
        return ""
    for style, threshold_value in kwargs.items():
        if threshold_value[0] is None and value <= threshold_value[1]:
            return style
        elif threshold_value[1] is None and value >= threshold_value[0]:
            return style
        elif threshold_value[0] <= value <= threshold_value[1]:
            return style


def duration(value: float, type: str):
    milliseconds = 0
    if type == "duration_ms":
        milliseconds = int(value)
        seconds, milliseconds = divmod(milliseconds, 1000)
    else:
        seconds = int(value)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    n = 0
    duration_str = ""
    if days > 0:
        n += 1
        duration_str += f"{days} 天 "
    if hours > 0:
        n += 1
        duration_str += f"{hours} 小时 "
    if minutes > 0:
        n += 1
        duration_str += f"{minutes} 分 "
    if seconds > 0 and n < 3:
        n += 1
        duration_str += f"{seconds} 秒"
    if milliseconds > 0 and n < 3:
        n += 1
        duration_str += f" {milliseconds} 毫秒"
    return duration_str


def bytes_to_human(value):
    """
    将字节转换为人类可读的格式
    :param value:
    :return:
    """
    value = float(value)
    if value < 1024:
        return f"{value} B"
    elif value < 1024 * 1024:
        return f"{value / 1024:.2f} KB"
    elif value < 1024 * 1024 * 1024:
        return f"{value / 1024 / 1024:.2f} MB"
    else:
        return f"{value / 1024 / 1024 / 1024:.2f} GB"


def kilobytes_to_human(value):
    value = float(value)
    if value < 1024:
        return f"{value} KB"
    elif value < 1024 * 1024:
        return f"{value / 1024:.2f} MB"
    elif value < 1024 * 1024 * 1024:
        return f"{value / 1024 / 1024:.2f} GB"
    else:
        return f"{value / 1024 / 1024 / 1024:.2f} TB"


def format(value, type=None, **kwargs):
    if not value:
        return value
    if type == "int":
        return int(value)
    elif type == "float":
        return round(float(value), 2)
    elif type == "bytes":
        return bytes_to_human(value)
    elif type == "kilobytes":
        return kilobytes_to_human(value)
    elif type == "timestamp_ms":
        return datetime.fromtimestamp(value / 1000).strftime(kwargs.get("format", "%Y-%m-%d %H:%M:%S"))
    elif type == "timestamp_s":
        return datetime.fromtimestamp(value).strftime(kwargs.get("format", "%Y-%m-%d %H:%M:%S"))
    elif type == "duration_ms":
        return duration(value, type="duration_ms")
    elif type == "duration_s":
        return duration(value, type="duration_s")
    elif type == "percentage100":
        return round(float(value), 2)
    elif type == "percentage":
        return round(float(value) * 100, 2)
    else:
        return value


def enum(value, **kwargs):
    if not kwargs or not value:
        return value
    for enum_value, map in kwargs.items():
        if enum_value == value:
            return map
    else:
        return {}


def sort_values_by_header(A, B, C):
    # 将 A 列表和 B 列表构建成字典
    table_dict = dict(zip(A, [pair for pair in zip(*B)]))

    # 根据 C 列表的顺序对字典进行排序
    sorted_values = {}
    for header in C:
        if header in table_dict:
            sorted_values[header] = {"data": table_dict[header], "attributes": C[header]}
            del table_dict[header]  # 删除已处理的键值对

    # 将剩余的键值对放到结果的最后面
    for k, v in table_dict.items():
        sorted_values[k] = {"data": v, "attributes": {}}

    return sorted_values


if __name__ == '__main__':
    print(threshold(value=81, green=(0, 80), red=(80, 100)))
    print(format(value=60000, type="duration_ms"))
    print(format(value=1024 * 1024 * 1024, type="bytes"))
    print(f"Int: {format(222, 'int')}")
    print(f"Float: {format(3.14159, 'float')}")
    print(f"Bytes: {format(len(b'test'), 'bytes')}")
    print(f"Timestamp (ms): {format(1640000000000, 'timestamp_ms')}")
    print(f"Timestamp (s): {format(16400000, 'timestamp_s')}")
    print(f"Duration (ms): {format(16400000, 'duration_ms')}")
    print(f"Duration (s): {format(164000, 'duration_s')}")
    print(f"Percentage100: {format(75.01, 'percentage100')}")
    print(f"Percentage: {format(0.75, 'percentage')}")
    print(enum(value="online", online={"title": "在线", "style": "green"}))
