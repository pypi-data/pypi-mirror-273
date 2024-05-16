from sparrowTools.system_transform import system_to_new_system
from sparrowTools import SparrowTypeError
from sparrowTools import SparrowRangeError


def system_to_string(data: str, system: int) -> str:
    """
    将任意进制合法的进制转换为字符串
    :param data: 需要被转换的数据
    :param system: 当前数据的进制
    :return: 字符串
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
    bytes_data = [int(binary[i:i + 8], 2) for i in range(0, len(binary), 8)]
    string = bytes(bytes_data).decode('utf-8')
    return string


def string_to_system(string: str, system: int) -> str:
    """
    将任意字符转为任意进制的数据,超过36进制无法复原为字符串
    :param string: 需要被转换的数据
    :param system: 需要转换成的进制
    :return: 所需进制的数据
    """
    if type(string) is not str:
        raise SparrowTypeError("String type is must be string")
    if type(system) is not int:
        raise SparrowTypeError("System type is must be int")
    bytes_data = string.encode('utf-8')
    binary = ''.join(format(byte, '08b') for byte in bytes_data)
    system = system_to_new_system(binary, 2, system)
    return system
