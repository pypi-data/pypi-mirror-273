from sparrowTools import SparrowTypeError


def system_to_new_system(data: str, old_system: int, new_system: int) -> str:
    """
    将任意进制转为其他任意进制
    :param data: 需要被转换的数据
    :param old_system: 现在数据的进制
    :param new_system: 需要被转成的进制
    :return: 新的进制数据
    """
    if type(data) is not str:
        raise SparrowTypeError("Data type is must be string")
    if type(old_system) is not int:
        raise SparrowTypeError("Old system type is must be int")
    if type(new_system) is not int:
        raise SparrowTypeError("New system type is must be int")
    data = int(data, old_system)
    anything = ""
    while data > 0:
        data_digit = data % new_system
        if data_digit > 9:
            data_digit = chr(data_digit - 10 + ord('A'))
        else:
            data_digit = str(data_digit)
        anything = data_digit + anything
        data //= new_system
    return anything if anything else '0'

