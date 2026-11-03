"""测试共享的夹具与辅助函数。

`Element` 的取值可能是 `set`、`tuple` 或标量，直接比较字典会因为容器类型不同而
误判，所以统一用 `norm_ev` 把 `Evidence` 规整成"可比较键 -> 浮点值"的普通字典：
集合型取值转成排序后的元组，排列型取值保留顺序，标量原样保留。
"""

from collections import defaultdict

import pytest

from dstz.core.atom import Element
from dstz.core.distribution import Evidence


def freeze(value):
    """把 `Element.value` 转成可比较、可哈希的规整形式。

    Args:
        value: `Element` 的取值，可能是 `set`、`tuple`、`str` 或其他标量。

    Returns:
        tuple | str: 集合型取值返回排序后的元组（丢弃集合的无序性），元组原样
            返回（RPS 里顺序有语义），标量原样返回。
    """
    if isinstance(value, (set, frozenset)):
        return tuple(sorted(value))
    return value


def norm_ev(ev, ndigits=12):
    """把 `Evidence` 转成普通字典，键用 `freeze` 规整、值四舍五入。

    Args:
        ev (Evidence): 待规整的证据分布。
        ndigits (int, optional): 浮点值保留的小数位数，用于吸收不同求和解序带来
            的末位差异。默认为 12。

    Returns:
        dict: 键为 `freeze` 后的取值，值为 `float`。
    """
    return {freeze(key.value): round(float(mass), ndigits)
            for key, mass in ev.items()}


def combine_reference(ev1, ev2, operation, renormalize):
    """按定义直接计算两条 mass function 的组合结果，作为被测实现的对照。

    该函数刻意不复用 `dstz` 里的任何组合逻辑：它枚举全部焦点元素对、按 `operation`
    算出合成命题并累加质量，从而独立校验实现。

    Args:
        ev1 (Evidence): 第一条 mass function。
        ev2 (Evidence): 第二条 mass function。
        operation (callable): 二元运算，DST 用 `set.intersection`/`set.union`。
        renormalize (bool): 为 `True` 时扣除空集质量并按 `1 - m(∅)` 归一化；
            为 `False` 时保留空集质量。

    Returns:
        dict: 与 `norm_ev` 同格式的结果字典。

    Raises:
        ValueError: `renormalize` 为 `True` 且两条证据完全冲突。
    """
    res = defaultdict(float)
    for key1, mass1 in ev1.items():
        for key2, mass2 in ev2.items():
            merged = operation(key1.value, key2.value)
            # set 不可哈希，先转 frozenset 才能作为累积字典的键
            res[frozenset(merged)] += mass1 * mass2
    if renormalize:
        conflict = res.pop(frozenset(), 0.0)
        total = 1.0 - conflict
        if total <= 0:
            raise ValueError("两证据完全冲突")
        res = {key: mass / total for key, mass in res.items()}
    return {freeze(key): round(mass, 12) for key, mass in res.items()}


@pytest.fixture(name="norm")
def fixture_norm():
    """提供 `norm_ev` 的夹具，供各测试模块直接调用。"""
    return norm_ev


@pytest.fixture(name="element_evidence")
def fixture_element_evidence():
    """构造一条混合 DST 证据 `{A: 0.2, AB: 0.3, BC: 0.5}`。

    Returns:
        Evidence: 焦点元素覆盖单元素、双元素与两种不同交集结构，便于检查
            `bel`/`pl`/`q` 与组合规则。
    """
    return Evidence({
        Element({'A'}): 0.2,
        Element({'A', 'B'}): 0.3,
        Element({'B', 'C'}): 0.5,
    })
