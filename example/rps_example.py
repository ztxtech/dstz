"""随机置换集（RPS）左正交规则的示例。

RPS 中 `Element` 的值是有序元组，顺序参与语义，因此正交和要按“有序交”计算。
`rps_left_rule` 以左证据的元素顺序为准取交，这里 `(1, 3, 2)` 与 `(2, 3)` 的有序交为
`(3, 2)`：`3` 在两者中同序，`2` 在左侧位于 `3` 之后。

预期输出（`python -m example.rps_example`）：:

    {(3, 2): 1.0}
"""

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.dual import rps_left_rule

# 恰好一条命题 (1, 3, 2)，质量为 1：对“顺序为 1-3-2”绝对确信
ev1 = Evidence({Element((1, 3, 2)): 1.0})

# 恰好一条命题 (2, 3)，质量为 1：对“顺序为 2-3”绝对确信
ev2 = Evidence({Element((2, 3)): 1.0})

# 左正交规则取有序交并校验两边的排列次序，结果的质量仍为 1
combined_ev = rps_left_rule(ev1, ev2)

print(combined_ev)
