class BaseConverter:
    def __init__(self, a: int, b: int):
        """
        将a进制的数字转换为b进制的数字
        :param a: 原数是a进制
        :param b: 转换后为b进制
        """
        self.a = a
        self.b = b
        # 检查输入是否在有效范围内
        if not 2 <= a <= 16 or not 2 <= b <= 16:
            raise ValueError("进制必须在[2, 16]范围内！")

        if not isinstance(a, int) or not isinstance(b, int):
            raise ValueError("进制必须是整数！")

    def convert(self, num: str):
        """
        将 a 进制的数字 number 转换为 b 进制
        :param num: a进制的数字对应的字符串
        :return: b进制的数字对应的字符串
        """
        # 检查输入是否是有效的数字

        try:
            int(num, self.a)
        except ValueError:
            raise ValueError(f"输入的不是一个 {self.a} 进制的有效数字！")

        flag = 0
        if num[0] == '-':
            flag = 1
            num = num[1:]

        # 将输入数字从 a 进制转换为十进制
        num_dec = 0
        for c in num:
            num_dec = num_dec * self.a + self._char_to_int(c)

        # 将十进制数字转换为 b 进制
        res = ""
        while num_dec > 0:
            r = num_dec % self.b
            res = self._int_to_char(r) + res
            num_dec //= self.b

        return '-' + res if flag else res

    def _char_to_int(self, c):
        """
        将字符转换为数字
        :param c:
        :return:
        """
        if c.isdigit():
            return int(c)
        else:
            c = c.upper()
            return ord(c) - ord('A') + 10

    def _int_to_char(self, n):
        """
        将数字转换为字符
        :param n:
        :return:
        """
        if n < 10:
            return str(n)
        else:
            return chr(ord('A') + n - 10)


# baseCon = BaseConverter(2, 10)
# print(baseCon.convert('-111'))