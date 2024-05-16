from sparrowTools import SparrowTypeError


class Data:
    def __getattr__(self, name):
        return None


def any_to_class(data: any) -> object:
    """
    将任意数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    dt = Data()
    if type(data) is dict:
        for k, v in data.items():
            if type(v) is dict:
                v = dict_to_class(v)
                setattr(dt, k, v)
            elif type(v) is list:
                list_data = []
                for i in v:
                    list_data.append(dict_to_class(i))
                setattr(dt, k, list_data)
            else:
                setattr(dt, k, v)
    elif type(data) is list:
        list_data = []
        for i in data:
            list_data.append(dict_to_class(i))
            setattr(dt, "data_transform", list_data)
    else:
        setattr(dt, "data_transform", data)
    return dt


def dict_to_class(data: dict) -> object:
    """
    将字典类型数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    if type(data) is not dict:
        raise SparrowTypeError("data_transform type is must be dict")
    dt = Data()
    for k, v in data.items():
        if type(v) is dict:
            v = dict_to_class(v)
            setattr(dt, k, v)
        elif type(v) is list:
            list_data = []
            for i in v:
                list_data.append(any_to_class(i))
            setattr(dt, k, list_data)
        else:
            setattr(dt, k, v)
    return dt


def list_to_class(data: list) -> object:
    """
    将数组类型数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    if type(data) is not list:
        raise SparrowTypeError("data_transform type is must be list")
    dt = Data()
    list_data = []
    for i in data:
        list_data.append(any_to_class(i))
    setattr(dt, "data_transform", list_data)
    return dt


def tuple_to_class(data: tuple) -> object:
    """
    将元祖类型数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    print(type(data))
    if type(data) is not tuple:
        raise SparrowTypeError("data_transform type is must be tuple")
    dt = Data()
    list_data = []
    for i in data:
        list_data.append(any_to_class(i))
        setattr(dt, "data_transform", list_data)
    return dt


def str_to_class(data: str) -> object:
    """
    将字符串类型数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    if type(data) is not str:
        raise SparrowTypeError("data_transform type is must be str")
    dt = Data()
    setattr(dt, "data_transform", data)
    return dt


def int_to_class(data: int) -> object:
    """
    将整数类型数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    if type(data) is not int:
        raise SparrowTypeError("data_transform type is must be int")
    dt = Data()
    setattr(dt, "data_transform", data)
    return dt


def float_to_class(data: float) -> object:
    """
    将浮点类型类型数据转换为嵌套类对象
    :param data: 需要转换的数据
    :return: 一个嵌套类
    """
    if type(data) is not float:
        raise SparrowTypeError("data_transform type is must be float")
    dt = Data()
    setattr(dt, "data_transform", data)
    return dt
