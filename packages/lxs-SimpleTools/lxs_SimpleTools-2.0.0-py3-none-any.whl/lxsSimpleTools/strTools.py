import re
import datetime


def get_string_length(string):
    """
    字符串长度：计算字符串的长度。
    """
    return len(string)


def convert_to_uppercase(string):
    """
    大小写转换：将字符串转换为大写。
    """
    return string.upper()


def convert_to_lowercase(string):
    """
    大小写转换：将字符串转换为小写。
    """
    return string.lower()


def remove_whitespace(string):
    """
    去除空格：去除字符串开头和结尾的空格。
    """
    return string.strip()


def split_string(string, delimiter):
    """
    分割字符串：按照指定的分隔符将字符串分割成列表。
    """
    return string.split(delimiter)


def join_strings(strings, delimiter):
    """
    连接字符串列表：将字符串列表连接成一个字符串。
    """
    return delimiter.join(strings)


def replace_substring(string, old_substring, new_substring):
    """
    替换子字符串：将字符串中的指定子字符串替换为新的字符串。
    """
    return string.replace(old_substring, new_substring)


def check_substring(string, substring):
    """
    检查子字符串是否存在：检查字符串中是否包含指定的子字符串。
    """
    return substring in string


def check_numeric(string):
    """
    判断字符串是否为数字：检查字符串是否表示一个有效的数字。
    """
    return string.isnumeric()


def capitalize_first_letter(string):
    """
    首字母大写：将字符串的首字母转换为大写。
    """
    return string.capitalize()


def reverse_string(string):
    """
    反转字符串：将字符串反转。
    """
    return string[::-1]


def check_prefix(string, prefix):
    """
    检查字符串是否以指定前缀开头：检查字符串是否以指定的前缀开始。
    """
    return string.startswith(prefix)


def check_suffix(string, suffix):
    """
    检查字符串是否以指定后缀结尾：检查字符串是否以指定的后缀结尾。
    """
    return string.endswith(suffix)


def count_substring(string, substring):
    """
    计算子字符串出现次数：计算字符串中指定子字符串出现的次数。
    """
    return string.count(substring)


def remove_special_characters(string):
    """
    去除特殊字符：去除字符串中的特殊字符或指定的字符。
    """
    return re.sub('[^A-Za-z0-9]+', '', string)


def check_empty(string):
    """
    检查字符串是否为空：检查字符串是否为空或只包含空格。
    """
    return string.strip() == ''


def get_substring(string, start, end):
    """
    获取字符串的子串：从字符串中提取指定位置的子串。
    """
    return string[start:end]


def check_palindrome(string):
    """
    检查字符串是否为回文：检查字符串是否为回文字符串（正反读都相同）。
    """
    return string == string[::-1]


def check_valid_date(string, format):
    """
    检查字符串是否为有效的日期：检查字符串是否表示一个有效的日期。
    """
    try:
        datetime.datetime.strptime(string, format)
        return True
    except ValueError:
        return False


def pad_string(string, length, character):
    """
    字符串填充：在字符串两侧填充指定字符以达到指定长度。
    """
    return string.ljust(length, character)


def extract_numbers(string):
    """
    提取数字：从字符串中提取数字部分。
    """
    return re.findall(r'\d+', string)
