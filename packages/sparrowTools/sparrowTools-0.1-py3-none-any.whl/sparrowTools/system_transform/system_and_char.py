from sparrowTools.system_transform import system_to_new_system
from sparrowTools import SparrowTypeError
from sparrowTools import SparrowRangeError


def system_to_char(data: str, system: int) -> str:
    """
    将任意进制合法的进制转换为字符
    :param data: 需要被转换的数据
    :param system: 当前数据的进制
    :return: 字符
    """
    if type(data) is not str:
        raise SparrowTypeError("Data type is must be string")
    if type(system) is not int:
        raise SparrowTypeError("System type is must be int")
    if system < 1 or system > 36:
        raise SparrowRangeError("System must be between 2 and 36")
    binary = system_to_new_system(data, system, 2)
    if len(binary) % 8 != 0:
        for i in range(8 - (len(binary) % 8)):
            binary = "0" + binary
    binary_groups = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    chars = [chr(int(group, 2)) for group in binary_groups]
    return ''.join(chars)


def char_to_system(char: str, system: int) -> str:
    """
    将任意字符转为任意进制的数据,超过36进制无法复原为字符
    :param char: 需要被转换的数据
    :param system: 需要转换成的进制
    :return: 所需进制的数据
    """
    if type(char) is not str:
        raise SparrowTypeError("Char type is must be string")
    if type(system) is not int:
        raise SparrowTypeError("System type is must be int")
    binary = ""
    for i in char:
        ascii_value = ord(i)
        binary += bin(ascii_value)[2:].zfill(8)
    system = system_to_new_system(binary, 2, system)
    return system
