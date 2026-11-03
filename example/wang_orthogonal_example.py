"""随机置换集上的 Wang Orthogonal Rule（`wang_orthogonal_rule`）示例。

两个证据各自给出两条有序命题，正交和按 `order_code_intersection` 求有序交、把质量
平均分配给交集结果，最后扣除与空集相交的质量并归一化。

预期输出（`python -m example.wang_orthogonal_example`）：:

    {('c', 'b'): 0.7826086956521741, ('a',): 0.2173913043478261}

数值来源：`('b', 'c')` 与 `('c', 'a', 'b')` 的有序交为 `('c', 'b')`，质量
`0.9 * 0.4 = 0.36`；两条 `'a'` 命题相交得 `('a',)`，质量 `0.1 * 0.6 + 0.1 * 0.4 =
0.10`；`('b', 'c')` 与 `'a'` 无公共元素，其 `0.9 * 0.6 = 0.54` 落到空集后被扣除，
余下质量除以 `1 - 0.54 = 0.46` 归一化。

注意 `Element(('a'))` 的括号里没有逗号，实际传的是字符串 `'a'` 而不是元组；两个规则
按可迭代对象逐字符取交，效果等同于单元素排列，合成结果再被重新包装成元组 `('a',)`。
"""

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.dual import wang_orthogonal_rule

# 第一个证据：一条双元素排列占 0.9，一条单元素命题占 0.1
ev1 = Evidence({
    Element(('b', 'c')): 0.9,
    Element(('a')): 0.1
})

# 第二个证据：一条三元素排列占 0.4，同样的单元素命题占 0.6
ev2 = Evidence({
    Element(('c', 'a', 'b')): 0.4,
    Element(('a')): 0.6
})

# 正交和按有序交合成，空集质量不参与分配，需归一化
ev = wang_orthogonal_rule(ev1, ev2)

print(ev)
