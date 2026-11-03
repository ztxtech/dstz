"""矩阵法实现的两类组合规则及其逆运算。

四个对外函数共享同一条流水线，差别只在变换矩阵与域内运算：

    disjunctive:  belief 域      bel = M_B · m，bel = bel1 ⊙ bel2，m = M_B^{-1} · bel
    conjunctive:  commonality 域 q   = M_Q · m，q   = q1   ⊙ q2，m = M_Q^{-1} · q
    de_*:         在同一个域内做逐点除法，用于"撤回"一次组合

其中 `M_B`、`M_Q` 分别是 `get_bfrm`、`get_qfrm` 生成的 Kronecker 幂矩阵，⊙ 为
逐元素乘。这里的 `disjunctive_rule` 走 BFRM（与并集语义一致），`conjunctive_rule`
走 QFRM（与交集语义一致），与 `dstz.evpiece.dual` 里同名函数的集合运算一致。

两条规则都不做冲突归一化：冲突质量留在空集分量上原样返回（质量之和仍为 1），是否
按 `1 - m(∅)` 归一化由调用方决定。

矩阵向量化要求两次输入落在同一 FoD 上：先取 `get_fod` 的并集再按它建向量，不在
该 FoD 内的焦点元素会被静默当成 0 质量，这是调用方需要保证的前提。
"""

import numpy as np

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.single import get_fod
from dstz.math.matrix.const import get_qfrm, get_bfrm
from dstz.math.matrix.func import get_ones_indices

# 反变换后小于该阈值的分量视为零：矩阵乘法在 2 ** n 维上累积的舍入误差约为
# 1e-17，远低于任何有意义的 mass 值。
_MASS_EPS = 1e-12


def matrix_rule(ev1, ev2, matrix, fod, mul=True, curItem=Element):
    """用给定的变换矩阵组合两个 mass 函数。

    流程固定为四步：

    1. 向量化：整数 i 的二进制第 j 位为 1 表示第 i 个分量对应集合含 `fod[j]`，
       i = 0 对应空集，同一套编码用于 `ev1` 与 `ev2`；
    2. 正变换 `v1 = matrix · m1`、`v2 = matrix · m2`；
    3. 域内逐点运算 `v = v1 * v2`（`mul=True`）或 `v = v1 / v2`（`mul=False`）；
    4. 反变换 `m = matrix^{-1} · v`，只把 `m[i] > 0` 的分量写回 `Evidence`。

    Args:
        ev1 (Evidence): 第一个 mass 函数。
        ev2 (Evidence): 第二个 mass 函数，焦点元素需与 `ev1` 落在同一个 FoD 上。
        matrix (np.ndarray): 形状为 `(2 ** n, 2 ** n)` 的可逆变换矩阵，通常由
            `get_qfrm` 或 `get_bfrm` 生成。
        fod (list): 有序的单元素列表，决定向量下标的编码顺序，长度 n 必须与
            `matrix` 规模匹配；不在其中的元素不会进入向量。
        mul (bool): `True` 时域内相乘（组合），`False` 时相除（逆组合）。
            默认为 `True`。
        curItem (callable): 仅为兼容签名保留，函数体未使用——输出元素固定由
            `Element` 构造。默认为 `Element`。

    Returns:
        Evidence: 组合结果。反变换后只保留大于 `_MASS_EPS` 的有限分量，因此零质量
        与浮点残渣（量级 1e-17 的舍入误差）不会写进结果；冲突保留在空集分量上，
        不做归一化，质量之和未必为 1。

    Raises:
        ValueError: `mul=False` 且除数在域内某分量为 0、而被除数在同一分量上不为
            0 时，这对输入不可能由该组合规则产生，逆组合无定义，抛出并给分量下标。
            两者同为 0 的分量取 0 作为一致解，不会报错。
        np.linalg.LinAlgError: `matrix` 不是二维方阵或不可逆时，`np.linalg.inv`
            抛出。

    Note:
        反变换结果理论上不应出现负质量，但浮点误差可能给出 -1e-16 量级的负值；
        这些分量同样小于 `_MASS_EPS`，会被丢弃。若出现明显负值，说明输入本身不是
        合法的 mass 函数，或矩阵与该 FoD 不匹配。
    """
    ev = Evidence()
    events = []
    # Create vector representations of the mass functions
    ev1_m = np.zeros(2 ** len(fod))
    ev2_m = np.zeros(2 ** len(fod))
    for i in range(2 ** len(fod)):
        event = set()
        event_index = get_ones_indices(i)
        if event_index:
            for j in get_ones_indices(i):
                event.add(fod[j])
        element = Element(event)
        events.append(element)
        if element in ev1:
            ev1_m[i] = ev1[element]
        if element in ev2:
            ev2_m[i] = ev2[element]

    # Transform, combine, and inverse-transform
    ev1_q = np.dot(matrix, ev1_m)
    ev2_q = np.dot(matrix, ev2_m)
    if mul:
        ev_q = ev1_q * ev2_q
    else:
        # 域内相除模拟"撤回"：乘积为 0 的分量无法唯一还原因子，分两种情况处理。
        # 除数为 0 且被除数也为 0 时，任意因子都能得到乘积 0，取 0 是一致的解；
        # 除数为 0 而被除数非 0 时，这对输入不可能是乘积的结果，直接报错。
        zeros = ev2_q == 0
        if zeros.any():
            violated = np.flatnonzero(zeros & (ev1_q != 0))
            if violated.size:
                raise ValueError(
                    f"除数的第 {violated.tolist()} 个域内分量为 0，但被除数不为 0，"
                    "这对输入无法由该组合规则产生，逆组合无定义")
            ev_q = np.zeros_like(ev1_q)
            ev_q[~zeros] = ev1_q[~zeros] / ev2_q[~zeros]
        else:
            ev_q = ev1_q / ev2_q
    matrix_inv = np.linalg.inv(matrix)
    ev_m = np.dot(matrix_inv, ev_q)

    # Convert the resulting vector back to an Evidence object
    for i in range(len(events)):
        if np.isfinite(ev_m[i]) and ev_m[i] > _MASS_EPS:
            ev[events[i]] = ev_m[i]
    return ev


def conjunctive_rule(ev1, ev2, curItem=Element):
    """用矩阵法实现交组合（QFRM）。

    FoD 取 `ev1` 与 `ev2` 单元素集合的并集并转成列表，变换矩阵为
    `get_qfrm(len(fod))`，即走 `matrix_rule` 的 `mul=True` 分支。与
    `dstz.evpiece.dual.ds_rule` 不同，这里不做冲突归一化：冲突质量留在空集分量上
    原样返回。

    Args:
        ev1 (Evidence): 第一个 mass 函数。
        ev2 (Evidence): 第二个 mass 函数。
        curItem (callable): 仅为兼容签名保留，未向下传递。默认为 `Element`。

    Returns:
        Evidence: 交组合结果，只保留反变换后大于阈值的有限分量；冲突质量留在
        空集分量上，不做归一化。
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_qfrm(len(fod)), fod)


def de_conjunctive_rule(ev1, ev2, curItem=Element):
    """用矩阵法实现交组合的逆运算（QFRM 域内相除）。

    在 commonality 域逐点相除，用于从 `ev1` 中撤回 `ev2` 的影响。要求 `ev2` 各个
    commonality 分量非零，否则撤回没有定义；反变换后只保留大于阈值的有限分量。

    Args:
        ev1 (Evidence): 被除的 mass 函数。
        ev2 (Evidence): 作为除数的 mass 函数。
        curItem (callable): 仅为兼容签名保留，未向下传递。默认为 `Element`。

    Returns:
        Evidence: 逆组合结果，只保留反变换后大于阈值的有限分量。

    Raises:
        ValueError: `ev2` 在 commonality 域某分量为 0，而 `ev1` 在同一分量上不为
            0 时抛出——`ev1` 不能是 `ev2` 与某个 mass 函数的交组合结果。两者同为
            0 的分量按 0 处理，不报错。
        np.linalg.LinAlgError: `matrix_rule` 在矩阵不可逆时抛出。
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_qfrm(len(fod)), fod, False)


def disjunctive_rule(ev1, ev2, curItem=Element):
    """用矩阵法实现并组合（BFRM）。

    FoD 取 `ev1` 与 `ev2` 单元素集合的并集并转成列表，变换矩阵为
    `get_bfrm(len(fod))`，即在 belief 域逐点相乘后反变换。冲突保留在空集分量上，
    不做归一化。

    Args:
        ev1 (Evidence): 第一个 mass 函数。
        ev2 (Evidence): 第二个 mass 函数。
        curItem (callable): 仅为兼容签名保留，未向下传递。默认为 `Element`。

    Returns:
        Evidence: 并组合结果，只保留反变换后大于阈值的有限分量；冲突质量留在空集
        分量上，不做归一化。
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_bfrm(len(fod)), fod)


def de_disjunctive_rule(ev1, ev2, curItem=Element):
    """用矩阵法实现并组合的逆运算（BFRM 域内相除）。

    在 belief 域逐点相除，用于从 `ev1` 中撤回 `ev2` 的影响。要求 `ev2` 的各个
    belief 分量非零：`bel(B) = 0` 表示该子集上没有任何支持，撤回方向不可逆。

    Args:
        ev1 (Evidence): 被除的 mass 函数。
        ev2 (Evidence): 作为除数的 mass 函数。
        curItem (callable): 仅为兼容签名保留，未向下传递。默认为 `Element`。

    Returns:
        Evidence: 逆组合结果，只保留反变换后大于阈值的有限分量。

    Raises:
        ValueError: `ev2` 在 belief 域某分量为 0（该子集上没有任何支持），而
            `ev1` 在同一分量上不为 0 时抛出；两者同为 0 的分量按 0 处理。
        np.linalg.LinAlgError: `matrix_rule` 在矩阵不可逆时抛出。
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_bfrm(len(fod)), fod, False)