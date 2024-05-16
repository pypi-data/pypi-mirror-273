import BaseConverter

class Bin():
    def __init__(self, num: str, b: int = 10):
        """
        :param num: 数字字符串
        :param base: num的进制，默认为10
        """
        if b != 2:
            num = BaseConverter(b, 2).convert(num)
        self.num = num

    def grey_to_bin(self):
        num = self.num
        if num[0] == '-': num = num[1:]
        res = num[0]

