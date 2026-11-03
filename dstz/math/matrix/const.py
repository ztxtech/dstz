"""矩阵法的变换矩阵常量。

矩阵法把 mass 函数写成 2^n 维向量，先左乘变换矩阵进入另一个域，在域内逐点运算，
再左乘逆矩阵回到 mass 域。这里给出 n = 1（单个单元素）时的两个基矩阵，高维版本由
`matrix_self_kron` 反复做 Kronecker 积得到：

    BFRM = [[1, 0], [1, 1]]
    QFRM = [[1, 1], [0, 1]]

与 `dstz.math.matrix.dual` 的用法对应：BFRM 用于 disjunctive 规则（变换到 belief
域），QFRM 用于 conjunctive 规则（变换到 commonality 域），`de_*` 则在同一个域内
做逐点除法。两个基矩阵的行列式都是 1，故任意次 Kronecker 幂都可逆，这是 `de_*`
规则成立的前提。
"""

import numpy as np

# Belief Function Relation Matrix (BFRM) for a single element.
# Used for transformations between mass functions and belief/plausibility functions.
BFRM = np.array([
    [1, 0],
    [1, 1]])

# Commonality Function Relation Matrix (QFRM) for a single element.
# Used for transformations between mass functions and commonality functions.
QFRM = np.array([
    [1, 1],
    [0, 1]])


def matrix_self_kron(matrix, n):
    """计算矩阵的 n 次 Kronecker 幂。

    从 1x1 单位矩阵出发反复调用 `np.kron`，等价于把 `matrix` 与自己做 n 次
    Kronecker 积；输入为 2x2 时结果形状为 `(2 ** n, 2 ** n)`。n = 0 时按定义返回
    1x1 单位矩阵，保证返回值始终可直接参与矩阵运算。

    Args:
        matrix (np.ndarray): 参与 Kronecker 积的方阵，通常为 `BFRM` 或 `QFRM`。
        n (int): Kronecker 幂次，必须为非负整数。

    Returns:
        np.ndarray: `(2 ** n * matrix.shape[0], 2 ** n * matrix.shape[1])` 的方阵；
        n = 0 时为 `np.ones((1, 1))`。

    Raises:
        ValueError: `n` 为负数时抛出。

    Example:
        >>> matrix_self_kron(QFRM, 2).shape
        (4, 4)
        >>> matrix_self_kron(QFRM, 0).tolist()
        [[1.0]]
    """
    if n < 0:
        raise ValueError(f"Kronecker 幂次必须为非负整数，实际为 {n}")
    res = np.ones((1, 1))
    for _ in range(n):
        res = np.kron(res, matrix)
    return res


def get_qfrm(n):
    """生成帧大小为 n 的公共函数关系矩阵 QFRM。

    返回 `QFRM` 的 n 次 Kronecker 幂，形状为 `(2 ** n, 2 ** n)`。按字典序把
    mass 向量写成 `m`、commonality 向量写成 `q`，则 `q = M_Q · m`，其中
    `M_Q` 即本函数返回值。

    Args:
        n (int): FoD 中单元素的个数。

    Returns:
        np.ndarray: 形状为 `(2 ** n, 2 ** n)` 的矩阵；n = 0 时为 `[[1.0]]`。
    """
    return matrix_self_kron(QFRM, n)


def get_bfrm(n):
    """生成帧大小为 n 的信任函数关系矩阵 BFRM。

    返回 `BFRM` 的 n 次 Kronecker 幂，形状为 `(2 ** n, 2 ** n)`。按字典序把
    mass 向量写成 `m`、belief 向量写成 `bel`，则 `bel = M_B · m`，其中
    `M_B` 即本函数返回值。

    Args:
        n (int): FoD 中单元素的个数。

    Returns:
        np.ndarray: 形状为 `(2 ** n, 2 ** n)` 的矩阵；n = 0 时为 `[[1.0]]`。
    """
    return matrix_self_kron(BFRM, n)