def string_split(string: str, length: int, sort: bool = False) -> list:
    """
    将字符串每四个分为一组并存入数组
    :param sort: 默认False,从前往后切割。True为从后往前切割
    :param length: 需要的长度
    :param string: 被切割的数据
    :return: 返回切割好的数据，类型为数组
    """
    result = []
    if sort:
        for i in range(0, len(string), length):
            result.append(string[::-1][i: i + length][::-1])
        return result[::-1]
    else:
        for i in range(0, len(string), length):
            result.append(string[i:i + length])
        return result



