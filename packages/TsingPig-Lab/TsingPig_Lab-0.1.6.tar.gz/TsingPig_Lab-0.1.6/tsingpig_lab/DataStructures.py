import math
from math import ceil
from typing import List

class ST:
    def __init__(self, nums: List, opt = lambda a, b: max(a, b)):
        """
        Initialize the Sparse Table (ST) data structure with the given list of numbers and an optional comparison function.

        :param nums: The list of numbers to preprocess.
        :param opt: The comparison function to use for queries. Default is max.
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
        Query the maximum value within the range [L, R].

        :param L: The left index of the range.
        :param R: The right index of the range.
        :return: The maximum value within the range [L, R].
        :rtype: object
        """
        k = self.log[R - L + 1]
        return self.opt(self.f[L][k], self.f[R - (1 << k) + 1][k])

