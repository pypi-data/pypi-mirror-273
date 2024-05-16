def 算数_保留小数点后指定位数(number, digits):
    """
    保留给定数值小数点后指定位数的函数。

    参数:
        number (float): 需要保留小数位的数值。
        digits (int): 保留的小数位数。

    返回:
        float: 保留小数点后指定位数后的数值。

    使用示例:
        result = 算数_保留小数点后指定位数(3.1415926, 2)
        print(result)  # 输出结果为 3.14
    """
    return round(number, digits)
