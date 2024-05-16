from sparrowTools import string_split
from sparrowTools import SparrowRangeError


def digital_to_chinese(number: str, is_large: bool = False) -> str:
    number = str(number).replace(",", '').replace("，", '')
    while True:
        if number[0] == "0":
            number = number[1::]
        else:
            break
    large_key = {
        "0": "零",
        "1": "壹",
        "2": "贰",
        "3": "叁",
        "4": "肆",
        "5": "伍",
        "6": "陆",
        "7": "柒",
        "8": "捌",
        "9": "玖"
    }
    small_key = {
        "0": "零",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九"
    }
    large_basics_unit = ["", "拾", "佰", "仟"]
    small_basics_unit = ["", "十", "百", "千"]
    if is_large:
        key = large_key
        basics_unit = large_basics_unit
    else:
        key = small_key
        basics_unit = small_basics_unit
    result = ''
    if len(number) > 72:
        raise SparrowRangeError("number is too long, must be at least 72")
    unit = ["万", "亿", "兆", "京", "垓", "秭", "穰", "沟", "涧", "正", "载", "极", "恒河沙",
            "阿僧祇", "那由他", "不可思议", "无量大数"]
    split_data = string_split(number, 4, True)[::-1]
    new_data = string_split(split_data[0], 1)[::-1]
    for j in range(len(new_data)):
        if new_data[j] == "0":
            result = "0" + result
        else:
            result = f"{new_data[j]}{basics_unit[j]}" + result
    unit_start = 0
    for i in split_data[1::]:
        if i != "0000":
            result_ = ""
            new_data = string_split(i, 1)[::-1]
            for j in range(len(new_data)):
                if new_data[j] == "0":
                    result_ = "0" + result_
                else:
                    result_ = f"{new_data[j]}{basics_unit[j]}" + result_
            for ij in range(len(new_data)):
                if result_[-1] == "0":
                    result_ = result_[:-1]
            result_ += unit[unit_start]
            result = result_ + result
        unit_start += 1
    for k, v in key.items():
        result = result.replace(k, v)
    zero_unit = []
    for i in basics_unit + unit:
        zero_unit.append("零" + i)
    for i in number:
        if result[-1] in zero_unit:
            result = result[:-1]
        elif result[-2::] in zero_unit:
            result = result[:-2]
        elif result[-3:] in zero_unit:
            result = result[:-3]
        else:
            break
    return result


print(digital_to_chinese(
    "106,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,123,000,000,000,000,000,000,000", True))
