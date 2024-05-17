class Version:
    """Version of the package"""

    __slots__ = ("number",)

    def __init__(self, num):
        self.number = num

    def __setattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    __delattr__ = __setattr__
