"""证据理论中三个基本信任函数：Bel、Pl 与 Q。

三个函数都对 mass 函数 `ev` 求和，求和范围由假设 `element`（记作 A）与各焦点元素
（`ev` 的键，记作 B）之间的集合关系决定：

    Bel(A) = Σ_{B ⊆ A, B ≠ ∅} m(B)
    Pl(A)  = Σ_{B ∩ A ≠ ∅, B ≠ ∅} m(B)
    Q(A)   = Σ_{B ⊇ A, B ≠ ∅} m(B)

三者统一忽略分配给空集的 `m(∅)`：`m(∅)` 表示“源自己就矛盾”的份额，若计入
似然会凭空抬高 Pl，使 `Bel(A) ≤ Pl(A) ≤ 1` 失效。于是恒有 `Bel(∅) = Pl(∅) = 0`
与 `Q(∅) = 1 - m(∅)`。

实现上都是对 `ev` 的一次遍历，不校验 `ev` 中各质量是否归一，也不做冲突处理；累加
初始值为整数 `0`，因此结果类型取决于 `ev` 中质量值的类型。

集合运算前统一用 `atom_set` 归一化：`Element.value` 为 `str`/`bytes` 等标量时
视作单元素原子，为 `set`/`tuple` 等容器时取其成员集合。这条约定让
`simple_space` 产出的标量原子与 `powerset` 产出的集合焦元走同一条计算路径；代价是
RPS 的有序焦元（`tuple`）会被展平成集合、顺序被忽略，需要保序语义时应改用
`dstz.evpiece.dual.rps_left_rule` 等专用算子。
"""

from dstz.core.atom import Element, atom_set
from dstz.core.distribution import Evidence


def pl(element, ev):
    """计算假设 A 的似然函数 Pl(A)。

    似然函数对所有与 A 交集非空的焦点元素的质量求和：

        Pl(A) = Σ_{B ∩ A ≠ ∅, B ≠ ∅} m(B)

    判空条件 `if key.value` 与 `bel`、`q` 保持一致，把空焦点元素排除在外，因此
    `Pl(∅) = 0`；若 A 与某焦点元素交集为空，该焦点的质量也不计入。实现不检查
    `ev` 是否已归一化，冲突质量同样不做扣除。

    Args:
        element (Element): 假设 A。`value` 可以是集合焦元，也可以是标量原子。
        ev (Evidence): mass 函数，键为 `Element`，值为质量。

    Returns:
        float: Pl(A)。没有任何焦点元素被计入时返回整数 `0`（累加初始值），
        否则返回各质量值累加后的类型。

    Example:
        >>> ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        >>> round(pl(Element({'B'}), ev), 12)
        0.6
    """
    hypothesis = atom_set(element.value)
    res = 0
    for key in ev:
        focal = atom_set(key.value)
        if focal and not focal.isdisjoint(hypothesis):
            res += ev[key]
    return res


def q(element, ev):
    """计算假设 A 的公共函数 Q(A)。

    公共函数对所有包含 A 的焦点元素的质量求和：

        Q(A) = Σ_{B ⊇ A, B ≠ ∅} m(B)

    判空条件 `if key.value` 排除了空焦点元素，但结果并不因此为 0：A 为空集时所有
    非空焦点元素都满足 A ⊆ B，故 Q(∅) 等于全部非空焦点元素质量之和（归一化 mass
    下为 1.0）。实现同样不检查 `ev` 的归一性。

    Args:
        element (Element): 假设 A。`value` 可以是集合焦元，也可以是标量原子。
        ev (Evidence): mass 函数，键为 `Element`，值为质量。

    Returns:
        float: Q(A)。没有任何焦点元素被计入时返回整数 `0`，否则返回各质量值
        累加后的类型。

    Example:
        >>> ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        >>> round(q(Element({'A', 'B'}), ev), 12)
        0.6
    """
    hypothesis = atom_set(element.value)
    res = 0
    for key in ev:
        focal = atom_set(key.value)
        if focal and hypothesis.issubset(focal):
            res += ev[key]
    return res


def bel(element, ev):
    """计算假设 A 的信任函数 Bel(A)。

    信任函数对所有 A 的子集焦点元素的质量求和：

        Bel(A) = Σ_{B ⊆ A, B ≠ ∅} m(B)

    判空条件 `if key.value` 排除空焦点元素，因此即使 `ev` 给空集分配了质量，
    Bel(∅) 仍为 0。实现不检查 `ev` 的归一性。

    Args:
        element (Element): 假设 A。`value` 可以是集合焦元，也可以是标量原子。
        ev (Evidence): mass 函数，键为 `Element`，值为质量。

    Returns:
        float: Bel(A)。没有任何焦点元素被计入时返回整数 `0`，否则返回各质量值
        累加后的类型。

    Example:
        >>> ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        >>> round(bel(Element({'A'}), ev), 12)
        0.4
    """
    hypothesis = atom_set(element.value)
    res = 0
    for key in ev:
        focal = atom_set(key.value)
        if focal and focal.issubset(hypothesis):
            res += ev[key]
    return res