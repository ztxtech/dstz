"""排列集合（permutation set）与有序交、顺序码交两类运算。

随机排列集（RPS）要求焦点元素带顺序，因此这里生成的 `Element` 取值统一是
`tuple`（而不是 DST 用到的 `set`），元组次序即排列次序。模块内提供三类运算：

* `permutation_set`：把单元素空间展开成所有“子集的全排列”，是 RPS 建模入口。
* `left_intersection`：Deng 提出的排列事件左交（left intersection, LI），
  “保留左排列中在右排列里出现过的元素，保持左侧次序与重复次数”。
* `order_code_intersection`：Wang 正交和使用的顺序码交，对两侧位置码按位取大，
  同一位置码上的并列元素拆成多条候选顺序。

`left_intersection` 与 `order_code_intersection` 是两个不同算子，前者单值、
后者多值，不可互相替换。

参考：
    Deng Y. Random permutation set. International Journal of Computers,
    Communications & Control, 2022, 17(1): 4542. 其中排列事件的左交（LI）与
    右交（RI）由定义 3.1 给出，右交是对右排列做同样过滤。
"""

import itertools
from itertools import combinations, permutations

from dstz.core.atom import Element


def _raw_atoms(items):
    """取出元素序列里的原始原子取值。

    `simple_space` 里的元素通常是 `Element`，而用户也可能直接传入裸标量
    （如 `{1, 2, 3}`）。两种写法都要能展开成“只含原始原子”的容器，否则
    `Element.value` 会退化成“装着 `Element` 的容器”，与
    `Element({'a'})`、`Element((1, 3, 2))` 这两类示例用法不一致。

    Args:
        items (Iterable): 待展开的元素序列，成员可以是 `Element` 或裸标量。

    Returns:
        list: 与输入等长的列表，`Element` 成员被替换为其 `.value`，其余成员
            原样保留。
    """
    return [getattr(item, "value", item) for item in items]


def permutation_set(simple_space, allow_empty=False):
    """枚举给定空间中所有子集的所有排列，每个排列包装成一个 `Element`。

    对子集大小从 `start_index` 枚举到 `len(simple_space)`，先用
    `itertools.combinations` 取子集，再对每个子集用 `itertools.permutations`
    展开其全部顺序，最后把每个顺序元组作为 `Element` 的取值。

    取值的成员是**原始原子**而不是 `Element`：输入若为 `{Element('A'),
    Element('B')}`，输出 `Element(()).value` 这一类容器里装的是 `'A'`、`'B'`
    这样的裸标量，与 `Element(('A', 'B'))` 完全等价，因此可以互相比较、也能被
    `len()` 与 `for` 直接消费（概率变换、信任函数都依赖这一点）。

    Args:
        simple_space (set): 待展开的元素集合，需要支持 `len()` 且可迭代；
            成员可以是 `Element`，也可以是裸标量。
        allow_empty (bool, optional): 为 `True` 时把空排列 `()` 计入结果，此时
            子集大小从 0 开始枚举。默认为 `False`。

    Returns:
        set: 由 `Element` 组成的集合，每个 `Element.value` 是一个原始原子构成的
            元组；重复出现的排列在集合中自动合并。

    Example:
        >>> s = {Element('A'), Element('B')}
        >>> sorted(x.value for x in permutation_set(s))
        [('A',), ('A', 'B'), ('B',), ('B', 'A')]
    """
    res = []
    start_index = 0 if allow_empty else 1
    for r in range(start_index, len(simple_space) + 1):
        for subset in combinations(simple_space, r):
            res.extend(permutations(subset))
    return {Element(tuple(_raw_atoms(perm))) for perm in res}


def left_intersection(a, b):
    """求两个排列事件的左交（left intersection, LI）。

    按 Deng 的定义，左交保留 `a` 中所有同时出现在 `b` 里的元素，次序沿用 `a`，
    重复次数也沿用 `a`：判据只看“元素是否在 `b` 中出现过”，因此 `a` 中重复出现
    的元素只要在 `b` 里出现一次就全部保留。

    结果一定是 `a` 的子序列（保序且不去重），但不保证是 `b` 的子序列——左交
    本身就是左偏的，这一点与右交（RI，保留 `b` 中出现在 `a` 里的元素）对称。

    Args:
        a (Iterable): 左排列，决定结果的次序与重复次数。
        b (Iterable): 右排列，只用于判定元素是否可出现。

    Returns:
        tuple: 左交结果；两侧没有公共元素时返回空元组 `()`。

    Example:
        >>> left_intersection((1, 3, 2), (2, 3))
        (3, 2)
        >>> left_intersection((1, 1, 2), (2,))
        (2,)
    """
    right = set(b)
    return tuple(x for x in a if x in right)


def order_code_intersection(a, b):
    """求两个有序序列的公共元素，并按合并后的位置码把它们排成若干顺序。

    这是 Wang 正交和使用的顺序码交，与 `left_intersection` 不是同一个算子。
    处理分三步：

    1. 先按 `a` 的顺序、再按 `b` 的顺序记录每个元素的出现下标，同一个元素在
       同侧重复出现时保留全部下标；随后对每个元素只取这些下标的最大值，作为
       它在合并顺序中的位置码（即两侧位置码按位取大）。
    2. 删掉只出现在一侧的元素（对称差），只保留交集。
    3. 按位置码把元素分组（位置码相同的元素落到同一组），组按位置码升序排列，
       再对各组做 `itertools.product`，把每一条组合路径拼成元组返回。

    第 3 步的产物是“每组各出一个元素”的元组，而不是组内元素的全排列。所以
    当多个公共元素的位置码相同时（例如两个序列互为逆序），它们会分散到不同的
    返回元组里，任一返回元组都不含全部公共元素。返回值因此是一组候选顺序，
    而不是唯一的合并结果；调用方（`wang_orthogonal_rule`）据此把质量平摊到
    多条候选上。

    Args:
        a (Iterable): 第一个有序序列。
        b (Iterable): 第二个有序序列。两个序列的元素都需要可哈希。

    Returns:
        list[tuple]: 候选顺序的列表，元组里装的是公共元素本身（不是下标）。
            交集为空时返回 `[()]`，因为 `itertools.product()` 无参数时产出一个
            空元组。

    Example:
        >>> order_code_intersection(('b', 'c'), ('c', 'a', 'b'))
        [('c', 'b')]
    """

    def swap_key_value(input_dict):
        """把“元素 -> 位置码”的字典翻转为“位置码 -> 元素列表”。

        同一个位置码对应多个元素时，这些元素按它们在原字典中的插入顺序追加到
        列表里，供调用方据此分组。

        Args:
            input_dict (dict): 待翻转的字典，值应当可哈希（用作新字典的键）。

        Returns:
            dict: 新字典，键是原字典的值，值是由原字典的键组成的列表。
        """
        output_dict = {}
        for key, value in input_dict.items():
            if value not in output_dict:
                output_dict[value] = [key]
            else:
                output_dict[value].append(key)
        return output_dict

    res = {}
    excluded_samples = set(a).union(set(b)) - set(a).intersection(set(b))

    # 先记录元素在 a 中的全部下标
    for idx, sample in enumerate(a):
        if sample not in res:
            res[sample] = [idx]
        else:
            res[sample].append(idx)

    # 再补上元素在 b 中的下标，两侧下标合在一起取最大值
    for idx, sample in enumerate(b):
        if sample not in res:
            res[sample] = [idx]
        else:
            res[sample].append(idx)

    # 逐键改值，字典大小不变，因此可在遍历 keys() 时原地更新
    for sample in res.keys():
        res[sample] = max(res[sample])

    for sample in excluded_samples:
        if sample in res:
            res.pop(sample)

    # 按位置码分组：键相同的元素进入同一个列表
    res = swap_key_value(res)
    # 组间按位置码升序排列，保证顺序来自 a、b 的合并结果
    res = [res[key] for key in sorted(res.keys())]
    # 每组取一个元素，拼出全部候选顺序
    res = [tuple(order) for order in itertools.product(*res)]
    return res
