"""单证据变换：信任度到概率、FoD 提取、Shafer 折扣、轮廓函数、温度变换。

本模块的函数都只依赖一条约定：`Element.value` 里装的是**原始原子**，DST 下是
`set`、RPS 下是 `tuple`，因此 `for atom in key.value` 拿到的就是可直接哈希的
标量（`'A'`、`1` 等），不需要再剥一层包装。
"""

import math

from dstz.core.atom import Element, atom_set
from dstz.core.distribution import Evidence
from dstz.math.func import pl


def pignistic_probability_transformation(ev):
    """把信度分布变换为赌徒概率分布（BetP）。

    BetP 把每个焦元的信度质量平均分给它包含的各个单元素原子：质量为 `m(A)` 的
    焦元 `A` 给每个 `a ∈ A` 分配 `m(A) / |A|`，再把同一原子的份额相加。这样得到
    的是各处相加为 1 的经典概率分布，可作为期望决策的依据。

    Args:
        ev (Evidence): 待变换的信度分布，键为 `Element`，质量为 `float`。

    Returns:
        Evidence: 新的 `Evidence`，键是单元素 `Element`（取值只有一个原始原子），
            值是 BetP 概率；质量总和为 1。

    Raises:
        ValueError: 存在空焦元（`A = ∅`，其 `.value` 长度为 0）时无法把质量平摊，
            直接报错而不是静默跳过。

    Example:
        >>> ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        >>> {str(k): round(v, 2) for k, v in pignistic_probability_transformation(ev).items()}
        {'A': 0.7, 'B': 0.3}
    """
    res = Evidence()
    for key in ev:
        size = len(key)
        if size == 0:
            raise ValueError(f"焦元 {key} 为空集，无法做赌徒概率变换")
        share = ev[key] / size
        for atom in key.value:
            s_item = Element(atom)
            if s_item in res:
                res[s_item] += share
            else:
                res[s_item] = share
    return res


def get_fod(ev):
    """提取证据的辨识框架（Frame of Discernment, FoD）。

    遍历所有焦元，把各自的原子并起来，得到"可能出现的单个取值"集合。原子由
    `atom_set` 规整：焦点元素的 `set`/`tuple` 取值取成员，`Element('A')` 这类
    标量取值取自身，因此单元素焦元与多元素焦元可以混用。

    Args:
        ev (Evidence): 证据分布。

    Returns:
        set: 由原始原子构成的集合，不含 `Element` 包装。`Element('AB')` 视为
            单个原子 `'AB'`，不会被拆成 `'A'` 与 `'B'`。

    Example:
        >>> sorted(get_fod(Evidence({Element({'A', 'B'}): 1.0})))
        ['A', 'B']
        >>> sorted(get_fod(Evidence({Element('AB'): 1.0})))
        ['AB']
    """
    res = set()
    for ele in ev.keys():
        res |= atom_set(ele.value)
    return res

def shafer_discounting(ev, alpha, fod=None):
    """对证据做 Shafer 折扣，把不可信部分转给辨识框架。

    信息源的可信度为 `alpha` 时，每个焦元的质量乘以 `alpha`，剩余
    `1 - alpha` 整体交给全集 `fod`（表示“完全不知道”）。折扣后各质量之和仍为 1：
    `alpha * Σm + (1 - alpha) = 1`。

    Args:
        ev (Evidence): 待折扣的证据分布。
        alpha (float): 可信度，取值须在 `[0, 1]` 内；1 表示完全可信，0 表示
            完全不可信（全部质量转给全集）。
        fod (set, optional): 预设的辨识框架（原始原子构成的集合）。为 `None` 时
            用 `get_fod(ev)` 现算；传入时必须非空。

    Returns:
        Evidence: 折扣后的新 `Evidence`，可能多出一个取值为 `fod` 的焦元。

    Raises:
        ValueError: `alpha` 不在 `[0, 1]` 内，或显式传入的 `fod` 为空集时。

    Example:
        >>> ev = Evidence({Element({'A'}): 0.6, Element({'A', 'B'}): 0.4})
        >>> sorted((sorted(k.value), round(v, 2)) for k, v in shafer_discounting(ev, 0.8).items())
        [(['A'], 0.48), (['A', 'B'], 0.52)]
    """
    if not 0 <= alpha <= 1:
        raise ValueError(f"可信度 alpha 必须位于 [0, 1] 内，当前为 {alpha}")

    res = Evidence()
    if fod is None:
        fod = get_fod(ev)
    if not fod:
        raise ValueError("辨识框架为空，无法把不可信质量转给全集")
    fod_element = Element(fod)

    # 每个焦元先按可信度打折
    for key, value in ev.items():
        res[key] = alpha * value

    # 不可信部分 (1 - alpha) 整体交给全集
    if fod_element in res:
        res[fod_element] += 1 - alpha
    else:
        res[fod_element] = 1 - alpha

    return res


def contour_transformation(ev):
    """把证据变换为轮廓函数（contour function）。

    轮廓函数给辨识框架中的每个单元素原子赋予它的似然度 `Pl({θ})`，是
    `pl` 在单元素集合上的映射结果；它不保证各值之和为 1，但可以看作“每个取值
    可能成立的程度”。

    Args:
        ev (Evidence): 证据分布。

    Returns:
        Evidence: 新的 `Evidence`，键为单元素 `Element`，值为对应似然度。
    """
    fod = get_fod(ev)
    res = Evidence()
    for event in fod:
        res[Element({event})] = pl(Element({event}), ev)
    return res


def temperature_transformation(ev, t):
    """对证据做温度变换并按焦元基数缩放。

    先算“归一化质量” `m(A) / (2^{|A|} - 1)`，再取 `t` 次幂，最后乘回同一分母：

    .. math::

        m_t(A) \\propto \\left(\\frac{m(A)}{2^{|A|} - 1}\\right)^{t} (2^{|A|} - 1)

    `t = 1` 时各值与输入相同（只差归一化），`t > 1` 会放大质量分布原本的差异，
    `t < 1` 会让分布更平。分母 `2^{|A|} - 1` 是焦元 `A` 在排除空集后的幂集
    大小，用来抵消“大焦元天然分到更多质量”的偏置。

    Args:
        ev (Evidence): 输入证据分布。
        t (float): 温度参数，`t = 0` 时输出退化为均匀分布。

    Returns:
        Evidence: 变换后并按总和归一化的新 `Evidence`，键与输入一致。

    Raises:
        ValueError: 存在空焦元（分母为 0），或变换后总和为 0（无法归一化）时。

    Example:
        >>> ev = Evidence({Element({'A'}): 0.5, Element({'A', 'B'}): 0.5})
        >>> sorted((sorted(k.value), round(v, 2)) for k, v in temperature_transformation(ev, 2.0).items())
        [(['A'], 0.75), (['A', 'B'], 0.25)]
    """
    res = Evidence()
    for key, value in ev.items():
        scale = 2 ** len(key) - 1
        if scale == 0:
            raise ValueError(f"焦元 {key} 为空集，温度变换的分母为 0")
        res[key] = math.pow(value / scale, t) * scale

    # 归一化，保证质量之和为 1
    norm_factor = sum(res.values())
    if norm_factor == 0:
        raise ValueError(
            f"温度变换后的质量总和为 0（t={t}），无法归一化；"
            "请检查输入质量是否含 0 且 t 为负"
        )
    for key, value in res.items():
        res[key] = value / norm_factor

    return res
