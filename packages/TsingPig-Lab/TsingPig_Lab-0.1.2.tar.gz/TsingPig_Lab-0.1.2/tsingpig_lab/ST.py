import math
from math import ceil
from typing import List

class ST:
    def __init__(self, nums: List, opt = lambda a, b: max(a, b)):
        """
        在 O(nlogn) 的时间内预处理数组 nums，使得查询区间[L, R]opt的时间复杂度为 O(1)。
        :param nums: 数组
        :param opt: 比较函数，默认为最值
        """
        n = len(nums)
        log = [0] * (n + 1)
        for i in range(2, n + 1):
            log[i] = log[i >> 1] + 1
        lenj = ceil(math.log(n, 2)) + 1
        f = [[0] * lenj for _ in range(n)]
        for i in range(n): f[i][0] = nums[i]
        for j in range(1, lenj):
            for i in range(n + 1 - (1 << j)):
                f[i][j] = opt(f[i][j - 1], f[i + (1 << (j - 1))][j - 1])
        self.f = f
        self.log = log
        self.opt = opt


    def qry(self, L: int, R: int):
        """
        查询区间 [L, R] 的最值（时间复杂度：O(1)）
        :rtype: object
        """
        k = self.log[R - L + 1]
        return self.opt(self.f[L][k], self.f[R - (1 << k) + 1][k])

