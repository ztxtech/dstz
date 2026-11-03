"""由单元素空间派生幂集（powerset）的工具函数。

这里提供 Dempster-Shafer 建模最常用的两步：先造一个简单的字母空间，再求它
的幂集；幂集里的每个焦元都被包装成 `Element`，其 `value` 是一个 `set`。
"""

from itertools import combinations

from dstz.core.atom import Element


def _raw_atoms(items):
    """取出元素序列里的原始原子取值。

    `simple_space` 里的元素通常是 `Element`，而用户也可能直接传入裸标量
    （如 `{'a', 'b'}`）。两种写法都要能展开成“只含原始原子”的容器，否则
    `Element.value` 会退化成“装着 `Element` 的容器”，与 `Element({'a'})`
    这类示例用法不一致（`bel`、`pl` 会对 `.value` 直接调用 `issubset`、
    `intersection`，装着 `Element` 时会报 `AttributeError`）。

    Args:
        items (Iterable): 待展开的元素序列，成员可以是 `Element` 或裸标量。

    Returns:
        list: 与输入等长的列表，`Element` 成员被替换为其 `.value`，其余成员
            原样保留。
    """
    return [getattr(item, "value", item) for item in items]


def simple_space(n):
    """生成由前 `n` 个大写字母组成的单元素空间。

    第 i 个元素的取值是 `chr(ord('A') + i)`，即从 `'A'` 开始按字母表顺序
    取连续的大写字母。函数不校验 `n`：
        - `n <= 0` 时返回空集合；
        - `n > 26` 时 `chr` 会给出字母表之外的字符（如 `'['`）。
    因为取值不可哈希的情况不会出现，返回的 `set` 天然去重。

    Args:
        n (int): 元素个数，作为 `range()` 的上界使用。

    Returns:
        set: 由 `Element` 组成的集合，元素取值为 `'A'`、`'B'` 等。

    Raises:
        ValueError: `n` 过大，使 `chr()` 收到的码位超出 Unicode 允许范围时
            由 `chr()` 抛出，本函数不拦截。

    Example:
        >>> sorted(str(x) for x in simple_space(3))
        ['A', 'B', 'C']
    """
    return {Element(chr(ord('A') + i)) for i in range(n)}


def powerset(simple_space, allow_empty=False):
    """求给定元素集合的幂集，每个子集包装成一个 `Element`。

    对参数中的元素做 `itertools.combinations`，按子集大小从 `start_index`
    枚举到 `len(simple_space)`，再把每个组合里的**原始原子**收集成 `set` 后
    包进 `Element`，最后用集合推导式收集，因此结果无序且重复子集自动合并。

    取值的成员是原始原子而不是 `Element`：输入若为 `{Element('A'),
    Element('B')}`，输出的 `Element({'A', 'B'})` 与手工构造的写法完全一致，
    于是 `bel`、`pl`、`q` 可以直接对 `.value` 做 `issubset`、`intersection`
    运算，不必再处理嵌套包装。

    参数名 `simple_space` 与模块级同名函数相互遮蔽，函数体内它指的是传入的
    集合，不会调用上面的 `simple_space`。

    Args:
        simple_space (set): 参与求幂集的元素集合，需要支持 `len()` 与
            `itertools.combinations`（即可迭代）；成员可以是 `Element`，也可以
            是裸标量。
        allow_empty (bool, optional): 为 `True` 时把空集计入结果，此时
            组合从大小 0 开始枚举。默认为 `False`。

    Returns:
        set: 由 `Element` 组成的集合，每个 `Element.value` 是参数的一个子集
            （由原始原子构成的 `set`）；`allow_empty=True` 时包含
            `Element(set())`。

    Example:
        >>> s = {Element('A'), Element('B')}
        >>> sorted(tuple(sorted(x.value)) for x in powerset(s, allow_empty=True))
        [(), ('A',), ('A', 'B'), ('B',)]
    """
    res = []
    start_index = 0 if allow_empty else 1
    for r in range(start_index, len(simple_space) + 1):
        res.extend(combinations(simple_space, r))
    return {Element(set(_raw_atoms(element))) for element in res}
