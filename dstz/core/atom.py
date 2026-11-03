"""证据理论中的原子对象：可标识、可比较、可哈希的元素。

这里定义两个字面量（literal）层的类：
    - `Item`：抽象基类，用 `idattr` 声明的属性集合作为身份标识，统一提供
      `__eq__` 与 `__hash__`。
    - `Element`：`Item` 的具体实现，把一个取值包装成证据元素。取值形态由
      上层模块约定：Dempster-Shafer（DST）框架里 `value` 是 `set`（焦元），
      Random Permutation Set（RPS）框架里 `value` 是 `tuple`（有序排列）。
"""

from abc import ABC, abstractmethod
from typing import Hashable

class Item(ABC):
    """以指定属性集合作为身份标识的抽象基类。

    子类必须实现 `idattr` 属性，列出参与身份判定的属性名；`__eq__` 与
    `__hash__` 都只依赖这些属性，其余属性不影响相等性与哈希。

    Attributes:
        _value (Any): 预留给子类的内部槽位，基类只把它置为 `None`，
            `Element` 并不使用它。
    """

    def __init__(self):
        """初始化 `Item`，把内部槽位 `_value` 置为 `None`。"""
        self._value = None

    @property
    @abstractmethod
    def idattr(self):
        """返回参与身份判定的属性名序列。

        子类必须实现本属性。列出的名字要能被 `getattr` 取到，取值可哈希
        （或可被 `frozenset()` 转换，详见 `__hash__`），因为相等性与哈希都
        按这些属性计算。

        Returns:
            list 或 tuple：属性名序列，例如 `['value']`。
        """
        pass

    def __eq__(self, other):
        """按 `idattr` 列出的属性比较两个对象是否相等。

        先做类型检查：`other` 必须是 `type(self)` 的实例（`isinstance`
        判定，因此子类实例也满足），否则直接返回 `False`，不返回
        `NotImplemented`，与不可比较对象比较时不会触发反向比较。随后逐项
        比较标识属性的取值。

        Args:
            other (Any): 待比较的对象。

        Returns:
            bool: 类型匹配且所有标识属性取值都相等时为 `True`，否则为
                `False`。
        """
        if not isinstance(other, type(self)):
            return False
        return all(getattr(self, attr) == getattr(other, attr) for attr in self.idattr)

    def __hash__(self):
        """按 `idattr` 属性的取值计算哈希值。

        逐个取标识属性，取值不可哈希时（`isinstance(value, Hashable)`
        为假，例如 `set`、`list`）先用 `frozenset(value)` 转换，再对属性
        元组求哈希。因此标识属性的取值必须可迭代且元素可哈希，否则
        `frozenset()` 会抛出 `TypeError`，本方法不做捕获。集合型取值经
        无序化后参与哈希，两个只差元素顺序的相等对象哈希值相同。

        Returns:
            int: 由标识属性元组算出的哈希值。
        """
        attrs = []
        for attr in self.idattr:
            value = getattr(self, attr)
            if not isinstance(value, Hashable):
                value = frozenset(value)
            attrs.append(value)
        return hash(tuple(attrs))


class Element(Item):
    """把单个取值包装成证据元素的基本单位。

    身份完全由 `value` 决定。`Element` 本身不校验取值类型，取值形态由使用
    场景约定：DST 中以 `set` 承载焦元（如 `Element({'A', 'B'})`），RPS 中以
    `tuple` 承载有序排列（如 `Element((1, 3, 2))`）。

    Attributes:
        value (Any): 元素承载的取值，默认 `None`。
    """

    def __init__(self, value=None):
        """初始化 `Element` 并保存取值。

        Args:
            value (Any, optional): 元素取值，原样保存，不做拷贝、不做类型
                检查。默认为 `None`。
        """
        super(Element, self).__init__()
        self.value = value

    @property
    def idattr(self):
        """返回身份标识属性名。

        Returns:
            list: 固定为 `['value']`，即相等性与哈希只取决于 `value`。
        """
        return ['value']

    def __str__(self):
        """返回取值的文本形式，不带 `Element(...)` 外壳。

        等价于 `str(self.value)`，例如 `str(Element({'A', 'B'}))` 得到
        `"{'A', 'B'}"`。

        Returns:
            str: `str(self.value)` 的结果。
        """
        return str(self.value)

    def __repr__(self):
        """返回与 `__str__` 完全一致的表示。

        因此 `Element` 被放进 set、dict、tuple 时，显示的是裸取值而不是
        `Element(...)`，调试输出依赖这一行为。

        Returns:
            str: `str(self.value)` 的结果。
        """
        return self.__str__()

    def __len__(self):
        """返回 `len(self.value)`，使 `len(element)` 可用。

        本类未定义 `__bool__`，真值判断因此走本方法：`Element(set())` 与
        `Element(())` 为假，非空取值则为真。

        Returns:
            int: `value` 的长度，对 set 即基数值。

        Raises:
            TypeError: `value` 不支持 `len()` 时（如 `int`）由内置 `len()`
                直接抛出，本方法不拦截。
        """
        return len(self.value)

    def __iter__(self):
        """按 `value` 的成员逐个产出，字符串与不可迭代取值都产出空序列。

        只要 `value` 有 `__iter__` 且不是 `str` 就逐个 `yield`；其余情况
        直接结束且不抛异常，所以 `list(Element('AB'))` 和
        `list(Element(3))` 都是空列表。字符串取值需要按整体
        （`element.value`）使用，不会被拆成字符。

        Yields:
            Any: `value` 中的一个成员。
        """
        if hasattr(self.value, '__iter__') and not isinstance(self.value, str):
            yield from self.value


def atom_set(value):
    """把 `Element.value` 规整成"搭在该取值上的原子集合"。

    `Element.value` 有两种形态：焦点元素持有原子容器（DST 为 `set`、RPS 为
    `tuple`），单元素焦点元素也可能直接持有裸标量（`Element('A')`，例如
    pignistic 变换的结果）。两种形态都要能回答"这个元素包含哪些原子"，本函数
    统一成集合：容器取值取成员，标量取值取自身，字符串按整体处理而不拆成字符。

    Args:
        value (Any): `Element` 的取值，可以是 `set`、`tuple`、`str` 或其他标量。

    Returns:
        set: 该取值对应的原子集合；标量与字符串返回单元素集合。
    """
    if isinstance(value, (str, bytes)) or not hasattr(value, '__iter__'):
        return {value}
    return set(value)
