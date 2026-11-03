"""最大熵 mass 函数的构造。

按最大熵原则分配质量：每个焦点元素的质量正比于它"内部组合数"，再整体归一化。子集型
空间（DST）与排列型空间（RPS）只差在生成器上，因此这里用生成器注入的方式共用同一套
权重计算与归一化流程。
"""

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.element.combination import simple_space, powerset
from dstz.element.permutation import permutation_set


def max_entropy_distribution(n, simple_generator, event_generator,
                             component_generator=set, condition_func=None):
    """在给定事件空间上构造最大熵 mass 函数。

    先由 `simple_generator(n)` 生成单元素空间 `ss`，再交给 `event_generator` 展开成
    候选事件 `es`；每个事件的权重取它内部组合的个数：

        w(A) = len(event_generator(component_generator(A)))
        m(A) = w(A) / Σ_{B ∈ es} w(B)

    给了 `condition_func` 时，`w(A)` 改用
    `len(condition_func(event_generator(component_generator(A))))`，即先按条件筛选
    再计数。权重越大、内部越"不确定"的事件分到越多质量，这正是最大熵的直觉。

    Args:
        n (int): 传给 `simple_generator` 的规模参数，即 FoD 中单元素的个数。
        simple_generator (callable): 由 `n` 生成单元素集合，如 `simple_space`。
        event_generator (callable): 由单元素集合生成候选事件，如 `powerset`、
            `permutation_set`；返回值需可迭代，元素需能被 `Element` 接受。
        component_generator (callable): 把事件还原成元素集合以计算内部组合数，默认
            为 `set`；对有序的排列型事件它同时起"忽略顺序"的作用。
        condition_func (callable, optional): 对 `event_generator(...)` 的结果再过滤
            一次，返回对象需支持 `len()`；默认 `None`，即不过滤。

    Returns:
        Evidence: 归一化后的 mass 函数，值之和为 1。权重为 0 的事件仍以 `0.0`
        质量保留在结果中，不会被删除。

    Raises:
        ZeroDivisionError: 所有事件权重之和为 0（如 `condition_func` 筛掉了全部
        结果，或事件空间为空）时，归一化除零。

    Note:
        结果的键按 `es` 的迭代顺序插入；权重由 `float(count)` 生成，因此所有质量
        都是 `float`。
    """

    res = Evidence()
    ss = simple_generator(n)
    # 物化成列表：下面要遍历两次，若传入的是一次性生成器，第二次会拿到空序列
    es = list(event_generator(ss))

    # Compute a weight for each event in the distribution.
    for element in es:
        # 生成器可能直接给 Element，也可能给裸取值（如无权重的原始元组）
        item = element if isinstance(element, Element) else Element(element)
        count = len(condition_func(event_generator(component_generator(item)))) \
            if condition_func else len(event_generator(component_generator(item)))
        res[item] = float(count)

    # Normalize the weights to create a valid distribution.
    states = sum(res.values())
    for item in res:
        res[item] /= states

    return res


def max_deng_entropy_distribution(n):
    """构造 Deng 熵意义下的最大熵 mass 函数。

    取 `simple_space(n)` 为单元素空间、`powerset` 为事件空间（不含空集），于是每个
    事件的权重是它的非空子集个数 `2 ** |A| - 1`：

        m(A) = (2 ** |A| - 1) / Σ_{B} (2 ** |B| - 1)

    该权重与 Deng 熵里的折扣因子一致；当输入质量全为正时，
    `temperature_transformation` 在 `t → 0` 的极限正是这个分布。

    Args:
        n (int): FoD 中单元素的个数。

    Returns:
        Evidence: 归一化后的 mass 函数。
    """
    return max_entropy_distribution(n, simple_space, powerset)


def max_rps_entropy_distribution(n):
    """构造 RPS 熵意义下的最大熵 mass 函数。

    取 `simple_space(n)` 为单元素空间、`permutation_set` 为事件空间，焦点元素是有序
    排列。焦距大小为 k 的事件，权重是它上面所有非空排列的个数：

        w(A) = Σ_{i=1..k} k! / (k - i)!

    再按 `max_entropy_distribution` 归一化。例如 n = 2 时四个焦点元素的质量为
    `(A): 0.1`、`(B): 0.1`、`(A, B): 0.4`、`(B, A): 0.4`。

    Args:
        n (int): FoD 中单元素的个数。

    Returns:
        Evidence: 归一化后的 mass 函数，键为排列构成的 `Element`。
    """
    return max_entropy_distribution(n, simple_space, permutation_set)