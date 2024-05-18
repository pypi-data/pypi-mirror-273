

# 进制转换器
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

    def convert(self, num: str) -> str:
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
            num_dec = num_dec * self.a + self.char_to_int(c)

        # 将十进制数字转换为 b 进制
        res = ""
        while num_dec > 0:
            r = num_dec % self.b
            res = self.int_to_char(r) + res
            num_dec //= self.b

        return '-' + res if flag else res

    def char_to_int(self, c: str) -> int:
        """
        将字符串形式的数字字符串，转换为整数
        :param c: 字符串表示的数字
        :return: 对应的整数
        """
        if c.isdigit():
            return int(c)
        else:
            c = c.upper()
            return ord(c) - ord('A') + 10

    def int_to_char(self, n: int) -> str:
        """
        将整数数字n转换为对应的字符串形式
        :param n: 整数
        :return: 对应的字符串
        """
        if n < 10:
            return str(n)
        else:
            return chr(ord('A') + n - 10)




# 二进制类
class Bin():
    def __init__(self, num: str, b: int = 2):
        """
        :param num: 数字字符串
        :param base: num的进制，默认为10
        """
        if b != 2:
            num = BaseConverter(b, 2).convert(num)
        self.num = num

    def grey_to_bin(self) -> str:
        """
        将当前的二进制码视为格雷码，求解其对应的二进制码
        :return: 对应的二进制码
        """
        num = self.num
        if num[0] == '-': num = num[1:]
        res = num[0]
        n = len(num)
        for i in range(1, n):
            res += str(int(res[-1]) ^ int(num[i]))
        return res

    def bin_to_grey(self) -> str:
        """
        将当前的二进制码视为二进制码，求解其对应的格雷码
        :return: 对应的格雷码
        """
        num = self.num
        if num[0] == '-': num = num[1:]
        n = len(num)
        res = num[0]
        for i in range(1, n):
            res += str(int(num[i - 1]) ^ int(num[i]))
        return res
