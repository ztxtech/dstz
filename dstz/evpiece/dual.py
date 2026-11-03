"""双证据组合规则：DS 规则、合取/析取规则、排列集左交与 Wang 正交和。

模块内的规则按“焦元里装的是什么代数”分为两组：

* `set` 取值的经典 DST 焦元：`conjunctive_rule`（合取，交）、`disjunctive_rule`
  （析取，并）、`ds_rule`（合取后再归一化，即 Dempster 规则）。
* `tuple` 取值的排列集（RPS）焦元：`rps_left_rule`（按左排列求交）、
  `wang_orthogonal_rule`（按顺序码求交）。

空集约定（全模块统一）：组合过程中产生的空集焦元 `m(∅)` 视为冲突，被丢弃后用
`1 - m(∅)` 归一化剩余质量；若冲突质量为 1（两证据完全矛盾）则无法归一化，直接
抛 `ValueError`，不返回总和为 0 的非法分布。
"""

import itertools

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.element.permutation import left_intersection, order_code_intersection


def _drop_empty_and_renormalize(res, empty_key):
    """丢掉空集焦元并用 `1 - m(∅)` 归一化剩余质量。

    组合规则产生空集时，其质量代表“两证据互相矛盾”的份额。本函数把它从结果中
    移除，再把剩余质量按比例放大到总和 1，这与 Dempster 规则的去冲突归一化一致。

    Args:
        res (Evidence): 就地修改的组合结果，不能包含 `empty_key` 之外的空集写法
            （`empty_key` 需与构造时用的类型一致，例如 `Element(set())` 或
            `Element(())`）。
        empty_key (Item): 表示空集的键，用于从 `res` 中取出冲突质量。

    Returns:
        Evidence: 同一个 `res` 对象，便于链式返回。

    Raises:
        ValueError: 冲突质量为 1，剩余质量为 0 无法归一化时。

    Side Effects:
        就地删除 `res` 中的 `empty_key` 并改写其余质量值。
    """
    empty_mass = res.pop(empty_key, None)
    if not empty_mass:
        return res
    denom = 1 - empty_mass
    if denom <= 0:
        raise ValueError(
            f"两证据完全冲突（冲突质量 m(∅) = {empty_mass}），无法用 1 - m(∅) 归一化"
        )
    for key in res.keys():
        res[key] = res[key] / denom
    return res


def ds_rule(ev1, ev2, curItem=Element):
    """用 Dempster-Shafer（DS）规则组合两个 DST 证据。

    对每一对焦元取交集、把质量相乘后累加，得到未归一化的合取结果；随后丢弃空集
    焦元 `m(∅)`，并用 `1 - m(∅)` 归一化，使输出质量之和回到 1。这就是经典
    Dempster 规则：它把“两个信息源互相矛盾”的份额当作可用信息重新分配。

    Args:
        ev1 (Evidence): 第一个证据，焦元取值必须是 `set`。
        ev2 (Evidence): 第二个证据，焦元取值必须是 `set`。
        curItem (callable, optional): 由交集构造新焦元的工厂，需要可哈希。默认
            `Element`；排列集场景下交集是元组，应改用能处理元组的类型。

    Returns:
        Evidence: 组合后的新 `Evidence`，质量之和为 1。

    Raises:
        ValueError: 两证据完全冲突（`1 - m(∅) = 0`）时。

    Example:
        >>> ev1 = Evidence({Element({'A'}): 0.8, Element({'A', 'B'}): 0.2})
        >>> ev2 = Evidence({Element({'B'}): 0.5, Element({'A', 'B'}): 0.5})
        >>> sorted((sorted(k.value), round(v, 3)) for k, v in ds_rule(ev1, ev2).items())
        [(['A'], 0.667), (['A', 'B'], 0.167), (['B'], 0.167)]
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.intersection(key2.value))
        mass = ev1[key1] * ev2[key2]
        if key in res:
            res[key] += mass
        else:
            res[key] = mass
    return _drop_empty_and_renormalize(res, curItem(set()))


def disjunctive_rule(ev1, ev2, curItem=Element):
    """用析取（disjunctive）规则组合两个 DST 证据，焦元取并集。

    析取规则把“至少一个源认为可能”的取值都保留下来，因此对每对焦元取**并集**、
    质量相乘后累加。并集不会为空（两侧焦元非空时），所以结果天然不需要去冲突
    归一化，质量之和为 1。

    注意与 `conjunctive_rule` 的方向：析取 = 并集，合取 = 交集；两者不可互换，
    否则大焦元会越并越大、小焦元会越交越小，语义完全相反。

    Args:
        ev1 (Evidence): 第一个证据，焦元取值必须是 `set`。
        ev2 (Evidence): 第二个证据，焦元取值必须是 `set`。
        curItem (callable, optional): 由并集构造新焦元的工厂，默认 `Element`。

    Returns:
        Evidence: 组合后的新 `Evidence`，质量之和为 1。

    Example:
        >>> ev1 = Evidence({Element({'A'}): 0.5, Element({'B'}): 0.5})
        >>> ev2 = Evidence({Element({'B'}): 0.5, Element({'C'}): 0.5})
        >>> sorted((sorted(k.value), v) for k, v in disjunctive_rule(ev1, ev2).items())
        [(['A', 'B'], 0.25), (['A', 'C'], 0.25), (['B'], 0.25), (['B', 'C'], 0.25)]
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.union(key2.value))
        mass = ev1[key1] * ev2[key2]
        if key in res:
            res[key] += mass
        else:
            res[key] = mass
    return res


def conjunctive_rule(ev1, ev2, curItem=Element):
    """用合取（conjunctive）规则组合两个 DST 证据，焦元取交集。

    合取规则要求“两个源同时认为可能”，因此对每对焦元取**交集**、质量相乘后累加。
    与 `ds_rule` 的差别在于这里**不做去冲突归一化**：落到空集上的质量会被保留为
    `m(∅)`，作为显式的冲突量，便于调用方自行处理（例如做冲突度分析）。若要去掉
    冲突并归一化，用 `ds_rule`。

    Args:
        ev1 (Evidence): 第一个证据，焦元取值必须是 `set`。
        ev2 (Evidence): 第二个证据，焦元取值必须是 `set`。
        curItem (callable, optional): 由交集构造新焦元的工厂，默认 `Element`。

    Returns:
        Evidence: 组合后的新 `Evidence`，可能含空集焦元，质量之和仍为 1。

    Example:
        >>> ev1 = Evidence({Element({'A'}): 0.5, Element({'A', 'B'}): 0.5})
        >>> ev2 = Evidence({Element({'B'}): 0.5, Element({'A', 'B'}): 0.5})
        >>> sorted((sorted(k.value), v) for k, v in conjunctive_rule(ev1, ev2).items())
        [([], 0.25), (['A'], 0.25), (['A', 'B'], 0.25), (['B'], 0.25)]
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.intersection(key2.value))
        mass = ev1[key1] * ev2[key2]
        if key in res:
            res[key] += mass
        else:
            res[key] = mass
    return res


def rps_left_rule(ev1, ev2, curItem=Element):
    """用排列集左交规则组合两个 RPS 证据。

    每次取 `ev1` 的一个焦元 `a` 与 `ev2` 的一个焦元 `b`，按 Deng 的左交定义求
    `left_intersection(a, b)`：保留 `a` 中同时出现在 `b` 里的元素，次序与重复
    次数沿用 `a`。因此结果总是 `a` 的子序列，`ev1` 在组合中处于“主导次序”的
    位置，规则名里的 left 即由此而来。

    组合完成后丢弃空元组 `()` 对应的冲突质量，用 `1 - m(∅)` 归一化，与
    `ds_rule` 的空集处理保持一致。

    Args:
        ev1 (Evidence): 左证据，焦元取值是可迭代的有序序列（通常是 `tuple`）。
        ev2 (Evidence): 右证据，焦元取值同上，只用于判定元素能否保留。
        curItem (callable, optional): 由元组构造新焦元的工厂，默认 `Element`；
            结果需要以元组为取值，因此不要传入会把元组拆成集合的类型。

    Returns:
        Evidence: 组合后的新 `Evidence`，键为元组形式的 `Element`，质量之和为 1。

    Raises:
        ValueError: 两证据完全冲突（`1 - m(∅) = 0`）时。

    Example:
        >>> ev1 = Evidence({Element((1, 3, 2)): 1.0})
        >>> ev2 = Evidence({Element((2, 3)): 1.0})
        >>> {str(k): v for k, v in rps_left_rule(ev1, ev2).items()}
        {'(3, 2)': 1.0}
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(left_intersection(key1.value, key2.value))
        mass = ev1[key1] * ev2[key2]
        if key in res:
            res[key] += mass
        else:
            res[key] = mass
    return _drop_empty_and_renormalize(res, curItem(()))


def wang_orthogonal_rule(ev1, ev2, curItem=Element):
    """用 Wang 正交和组合两个 RPS 证据。

    对每对焦元调用 `order_code_intersection` 求候选顺序：该算子按“两侧位置码取
    大”合并两边的次序，交集元素若落在同一位置码上会被拆成多条候选。得到 `n` 条
    候选顺序后，本规则把该对焦元的质量 `m1(A) * m2(B)` **平均分成 `n` 份**，每条
    候选各得一份。这与“单一交结果”的规则不同：前者是多值算子，质量必须在多个
    可能顺序之间平摊，否则总质量会凭空翻倍。

    组合完成后同样丢弃空元组冲突质量并归一化。

    参考：Wang Y., Li Z., Deng Y. A new orthogonal sum in Random Permutation Set.
    Fuzzy Sets and Systems, 2024, 109034.

    Args:
        ev1 (Evidence): 第一个 RPS 证据，焦元取值为有序序列。
        ev2 (Evidence): 第二个 RPS 证据，焦元取值为有序序列。
        curItem (callable, optional): 由元组构造新焦元的工厂，默认 `Element`。

    Returns:
        Evidence: 组合后的新 `Evidence`，键为元组形式的 `Element`，质量之和为 1。

    Raises:
        ValueError: 两证据完全冲突（`1 - m(∅) = 0`）时。

    Example:
        >>> ev1 = Evidence({Element(('b', 'c')): 0.9, Element(('a',)): 0.1})
        >>> ev2 = Evidence({Element(('c', 'a', 'b')): 0.4, Element(('a',)): 0.6})
        >>> sorted((sorted(k.value), round(v, 3)) for k, v in wang_orthogonal_rule(ev1, ev2).items())
        [(['a'], 0.217), (['b', 'c'], 0.783)]
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        cur_keys = [
            curItem(key) for key in order_code_intersection(key1.value, key2.value)
        ]
        share = ev1[key1] * ev2[key2] / len(cur_keys)
        for key in cur_keys:
            if key in res:
                res[key] += share
            else:
                res[key] = share
    return _drop_empty_and_renormalize(res, curItem(()))
