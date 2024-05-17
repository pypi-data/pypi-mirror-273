"""
列表工具
"""
import math
from typing import Any


def divide_to_groups(list_value: list[Any], group_length: int = 1000) -> list[list[Any]]:
    """
    将列表进行分组
    :param list_value: 列表值, 如：[1,2,3,4,5]
    :param group_length: 分组长度
    :return: 分组后的列表， 如：[[1,2],[3,4],[5]]
    """
    result_list = []
    group_count = math.ceil(len(list_value) / group_length)
    for i in range(group_count):
        result_list.append(list_value[i * group_length:(i + 1) * group_length])
    return result_list
