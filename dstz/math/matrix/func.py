"""矩阵法用到的编码辅助函数。

矩阵法把 2^n 个子集与 0 .. 2^n - 1 的整数一一对应：整数的二进制位标记该子集包含
哪些单元素。本模块只提供这一映射的逆向查询，正向组装由调用方完成。
"""


def get_ones_indices(n):
    """返回整数 n 的二进制表示中为 1 的位下标（升序）。

    矩阵法用整数编码集合：若 FoD 有 N 个单元素，则 `0 .. 2 ** N - 1` 的每个整数对应
    一个子集，二进制第 i 位为 1 表示该子集含第 i 个单元素。本函数给出这些位的下标。

    Args:
        n (int): 非负整数，通常落在 `0 .. 2 ** N - 1` 范围内。

    Returns:
        list: 位下标列表，升序且互不相同；`n = 0` 时为空列表。

    Raises:
        TypeError: `n` 为浮点数等非整数时，`n & 1` 无法执行。

    Note:
        负整数不受支持：`n >> 1` 对负数收敛到 -1 而不是 0，`while n` 永不结束。

    Example:
        >>> get_ones_indices(5)  # 二进制 101
        [0, 2]
        >>> get_ones_indices(10)  # 二进制 1010
        [1, 3]
    """
    indices = []
    index = 0
    while n:
        if n & 1:
            indices.append(index)
        n >>= 1
        index += 1
    return indices