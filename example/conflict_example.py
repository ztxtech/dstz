"""Dempster-Shafer 合成规则（`ds_rule`）的最小示例。

构造两个 mass function：第一个只信 `{A}`、`{B}`，第二个只信 `{C}`、`{B}`。二者在
`{B}` 上共识、在 `{A}` 与 `{C}` 上完全冲突，冲突质量按 Dempster 规则归一化后消失。

预期输出（`python -m example.conflict_example`）：:

    {{'B'}: 1.0000000000001101}

`{B}` 的质量理论值应为 1，打印出的末位偏差来自浮点运算，不是实现缺陷。
"""

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.dual import ds_rule

# 第一个 mass function：{A}、{B} 上各有 0.99、0.01 的质量
e1 = Evidence()
e1[Element({'A'})] = 0.99
e1[Element({'B'})] = 0.01

# 第二个 mass function：只在 {B} 上与 e1 重叠，{C} 与 {A} 互斥
e2 = Evidence()
e2[Element({'C'})] = 0.99
e2[Element({'B'})] = 0.01

# 冲突项 {A}∩{C} 为空，其质量被归一化除掉，因此结果只剩 {B}
e = ds_rule(e1, e2)

print(e)
