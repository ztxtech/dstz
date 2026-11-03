"""证据分布的容器：以 `Item` 为键、以浮点数为值的字典。

`Evidence` 是 `dict` 的子类，用来承载 mass function（基本概率分配）；键是
`Element` 等 `Item` 实例，值是浮点权重。类型约束只在两条路径上生效：
构造（`__init__`）与下标赋值（`__setitem__`）。
"""

from dstz.core.atom import Item


class Evidence(dict):
    """存放证据权重的字典，键为 `Item`、值为 `float`。

    在证据理论里用它表示 mass function：键是焦元（`Element`），值是对应的
    基本概率分配。构造与下标赋值都会做类型校验：
        - 键必须是 `Item` 实例，否则抛 `TypeError('Key must be an instance
          of Item')`；
        - 值必须是 `float`，`int` 也算不合法，否则抛
          `TypeError('Value must be a float')`（因此 `1` 不被接受，要写
          `1.0`）。

    校验不是全路径的。`dict.update()`、`dict.setdefault()`、`|=`（`__ior__`）
    走的是 `dict` 的 C 层实现，不经过 `__setitem__`，可以写入非法键值；
    `copy()` 返回的是普通 `dict` 而非 `Evidence`。需要保持约束时，用构造器
    或下标赋值重建对象。
    """

    def __init__(self, *args, **kwargs):
        """按 `dict` 的规则初始化，随后逐项校验键与值。

        参数原样交给 `dict.__init__`，插入完成后再遍历自身条目，先查键、
        再查值。因此非法条目抛异常时对象不会正常返回，但校验发生在插入
        之后，条目顺序决定第一个被检查到的非法项。

        Args:
            *args: 传给 `dict` 构造器的位置参数，如映射、可迭代键值对。
            **kwargs: 传给 `dict` 构造器的关键字参数。

        Raises:
            TypeError: 任一键不是 `Item` 实例，或任一值不是 `float`。
        """
        super(Evidence, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if not isinstance(key, Item):
                raise TypeError('Key must be an instance of Item')
            if not isinstance(value, float):
                raise TypeError('Value must be a float')

    def __setitem__(self, key, value):
        """校验通过后写入一对键值，键为 `Item`、值为 `float`。

        先查键再查值，任一不合格都不写入；通过校验才调用 `dict` 的实现，
        已存在的键会被覆盖。

        Args:
            key (Item): 证据元素，必须是 `Item` 实例。
            value (float): 与该键关联的权重。

        Raises:
            TypeError: 键不是 `Item` 实例，或值不是 `float`。
        """
        if not isinstance(key, Item):
            raise TypeError('Key must be an instance of Item')
        if not isinstance(value, float):
            raise TypeError('Value must be a float')
        super(Evidence, self).__setitem__(key, value)

    def __getitem__(self, item):
        """按键取值，并先校验键的类型。

        只校验键，不校验值；键不存在时按 `dict` 的语义抛出 `KeyError`。
        `ev.get(item)` 不走本方法，因此不触发校验。

        Args:
            item (Item): 要取值的键，必须是 `Item` 实例。

        Returns:
            float: 该键对应的权重。

        Raises:
            TypeError: 键不是 `Item` 实例。
            KeyError: 键类型合法但字典中不存在该键。
        """
        if not isinstance(item, Item):
            raise TypeError('Key must be an instance of Item')
        return super(Evidence, self).__getitem__(item)
