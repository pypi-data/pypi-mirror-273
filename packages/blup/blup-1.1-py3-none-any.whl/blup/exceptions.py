class BlupException(Exception):
    pass

class BlupIterableJson(BlupException):
    def __init__(self):
        super().__init__("Wrong json structure : top element needs to be an object")
