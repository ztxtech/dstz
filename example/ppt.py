"""Pignistic probability transformation 示例。

对一个只在 `{A, B, C}` 上赋 1.0 质量的证据做 pignistic 变换，观察质量如何均摊到单元素
命题，再用 Deng entropy 对比变换前后的不确定性。运行方式为
`python -m example.ppt`（在仓库根目录执行）。
"""

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.single import pignistic_probability_transformation
from dstz.math.stat.moment import deng_entropy

# 只含一条命题 {A, B, C} 的证据，全部质量都赋给它
ev = Evidence()
ev[Element({'A', 'B', 'C'})] = 1.0  # 质量值必须是 float，int 会被 __setitem__ 拒绝

print('primary: ', ev)

print('entropy', deng_entropy(ev))

# pignistic 变换把多元集合的质量按元素个数均摊给各单元素命题
bet_ev = pignistic_probability_transformation(ev)

print('after ppt: ', bet_ev)

print('entropy', deng_entropy(bet_ev))
