class SparrowTypeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is None:
            self.error_message = "type is error"
        else:
            self.error_message = error_message
        super().__init__(self.error_message)


class SparrowRangeError(Exception):
    def __init__(self, error_message: str = None):
        if error_message is None:
            self.error_message = "Index out of range"
        else:
            self.error_message = error_message
        super().__init__(self.error_message)
