import math


def 算数_向下取整(number):
    """
    向下取整函数，返回不大于给定数字的最大整数。

    参数:
        number (float): 需要向下取整的数字。

    返回:
        int: 不大于给定数字的最大整数。

    使用示例:
        print(算数_向下取整(3.8))  # 输出：3
        print(算数_向下取整(-3.8))  # 输出：-4
    """
    return math.floor(number)
