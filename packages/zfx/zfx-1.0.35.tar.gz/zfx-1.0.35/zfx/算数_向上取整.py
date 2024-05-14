import math


def 算数_向上取整(number):
    """
    向上取整数，返回不小于给定数字的最小整数。

    参数:
        number (float): 需要向上取整的数字。

    返回:
        int: 不小于给定数字的最小整数。
        None: 如果输入不是有效数字或遇到其他异常情况。

    使用示例:
        result = 算数_向上取整(3.4)
        print("结果:", result)  # 输出结果为 4
    """
    try:
        return math.ceil(number)
    except Exception:
        return None