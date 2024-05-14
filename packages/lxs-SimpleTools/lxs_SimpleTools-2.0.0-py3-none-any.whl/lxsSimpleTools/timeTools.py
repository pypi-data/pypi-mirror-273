import calendar
import datetime
import time


def format_current_time():
    """
    返回当前时间的格式化字符串，格式为 "%Y-%m-%d %H:%M:%S"。
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def format_custom_time(year, month, day, hour, minute, second):
    """
    将指定的年、月、日、时、分、秒格式化为字符串，格式为 "%Y/%m/%d %H:%M:%S"。
    参数：
        year: 年份
        month: 月份
        day: 日期
        hour: 小时
        minute: 分钟
        second: 秒钟
    返回值：
        格式化的时间字符串
    """
    custom_time = datetime.datetime(year, month, day, hour, minute, second)
    formatted_time = custom_time.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_time


def format_current_date():
    """
    返回当前日期的格式化字符串，格式为 "%Y-%m-%d"。
    """
    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%Y-%m-%d")
    return formatted_date


def format_current_time_only():
    """
    返回当前时间的格式化字符串，只包含时、分、秒，格式为 "%H:%M:%S"。
    """
    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime("%H:%M:%S")
    return formatted_time


def format_timestamp(timestamp):
    """
    将时间戳转换为格式化的字符串，格式为 "%Y-%m-%d %H:%M:%S"。
    参数：
        timestamp: 时间戳
    返回值：
        格式化的时间字符串
    """
    formatted_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def parse_time(time_str, format_str):
    """
    解析给定的时间字符串为时间对象，使用指定的格式字符串。
    参数：
        time_str: 时间字符串
        format_str: 格式字符串
    返回值：
        解析后的时间对象
    """
    parsed_time = datetime.datetime.strptime(time_str, format_str)
    return parsed_time


def convert_to_timestamp(time_obj):
    """
    将时间对象转换为时间戳。
    参数：
        time_obj: 时间对象
    返回值：
        时间戳
    """
    timestamp = datetime.datetime.timestamp(time_obj)
    return timestamp


def get_current_year():
    """
    返回当前年份。
    """
    current_year = datetime.datetime.now().year
    return current_year


def get_current_month():
    """
    返回当前月份。
    """
    current_month = datetime.datetime.now().month
    return current_month


def get_current_weekday():
    """
    返回当前星期几的数值表示，其中0表示星期一，6表示星期日。
    """
    current_weekday = datetime.datetime.now().weekday()
    return current_weekday


def get_current_time():
    """
    获取当前时间：获取当前的日期和时间。
    """
    return datetime.datetime.now()


def format_time(time, format):
    """
    格式化时间：将时间对象格式化为指定的字符串格式。
    参数：
        time: 时间对象
        format: 时间格式字符串
    返回值：
        格式化后的时间字符串
    """
    return time.strftime(format)


def get_year(time):
    """
    获取时间的年份：从时间对象中提取年份。
    参数：
        time: 时间对象
    返回值：
        年份
    """
    return time.year


def get_month(time):
    """
    获取时间的月份：从时间对象中提取月份。
    参数：
        time: 时间对象
    返回值：
        月份
    """
    return time.month


def get_date(time):
    """
    获取时间的日期：从时间对象中提取日期。
    参数：
        time: 时间对象
    返回值：
        日期对象
    """
    return time.date()


def get_hour(time):
    """
    获取时间的小时：从时间对象中提取小时。
    参数：
        time: 时间对象
    返回值：
        小时
    """
    return time.hour


def get_minute(time):
    """
    获取时间的分钟：从时间对象中提取分钟。
    参数：
        time: 时间对象
    返回值：
        分钟
    """
    return time.minute


def get_second(time):
    """
    获取时间的秒数：从时间对象中提取秒数。
    参数：
        time: 时间对象
    返回值：
        秒数
    """
    return time.second


def add_time(time, delta):
    """
    时间加减：对时间对象进行加减操作。
    参数：
        time: 时间对象
        delta: 时间增量（可以是正数或负数）
    返回值：
        计算后的时间对象
    """
    return time + delta


def subtract_time(time, delta):
    """
    时间加减：对时间对象进行加减操作。
    参数：
        time: 时间对象
        delta: 时间增量（可以是正数或负数）
    返回值：
        计算后的时间对象
    """
    return time - delta


def calculate_time_difference(time1, time2):
    """
    时间差计算：计算两个时间之间的时间差。
    参数：
        time1: 第一个时间对象
        time2: 第二个时间对象
    返回值：
        时间差（timedelta对象）
    """
    return time2 - time1


def compare_times(time1, time2):
    """
    时间比较：比较两个时间的先后顺序。
    参数：
        time1: 第一个时间对象
        time2: 第二个时间对象
    返回值：
        -1 表示 time1 在 time2 之前
         0 表示 time1 和 time2 相等
         1 表示 time1 在 time2 之后
    """
    if time1 < time2:
        return -1
    elif time1 > time2:
        return 1
    else:
        return 0


def parse_time(time_string, format):
    """
    时间字符串解析：将字符串解析为时间对象。
    参数：
        time_string: 时间字符串
        format: 时间格式字符串
    返回值：
        解析后的时间对象
    """
    return datetime.datetime.strptime(time_string, format)


def is_leap_year(year):
    """
    判断闰年：判断给定年份是否为闰年。
    参数：
        year: 年份
    返回值：
        True 表示是闰年
        False 表示不是闰年
    """
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def get_weekday(date):
    """
    获取指定日期的星期几：获取给定日期对应的星期几。
    参数：
        date: 日期对象
    返回值：
        星期几的字符串表示
    """
    return date.strftime('%A')


def get_days_in_current_month():
    """
    获取当前月份的天数：获取当前月份的总天数。
    返回值：
        当前月份的天数
    """
    now = datetime.datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def sleep(seconds):
    """
    时间睡眠：让程序暂停执行一段时间。
    参数：
        seconds: 睡眠时间（秒）
    """
    time.sleep(seconds)


def get_timestamp():
    """
    获取时间戳：获取当前时间的时间戳。
    返回值：
        时间戳（整数）
    """
    return int(datetime.datetime.now().timestamp())


def is_within_time_range(time, start_time, end_time):
    """
    判断时间是否在指定时间段内：检查给定时间是否在指定的时间段内。
    参数：
        time: 时间对象
        start_time: 时间段的开始时间
        end_time: 时间段的结束时间
    返回值：
        True 表示在时间段内
        False 表示不在时间段内
    """
    return start_time <= time <= end_time


def validate_time_format(time_string, format):
    """
    时间格式验证：验证给定的时间字符串是否符合指定的格式。
    参数：
        time_string: 时间字符串
        format: 时间格式字符串
    返回值：
        True 表示格式正确
        False 表示格式错误
    """
    try:
        datetime.datetime.strptime(time_string, format)
        return True
    except ValueError:
        return False


def convert_timestamp_to_time(timestamp):
    """
    时间戳转换：将时间戳转换为时间对象。
    参数：
        timestamp: 时间戳
    返回值：
        时间对象
    """
    return datetime.datetime.fromtimestamp(timestamp)
