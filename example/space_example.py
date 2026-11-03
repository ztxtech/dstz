"""幂集、置换集与最大熵分布的示例。

以长度为 2 的简单空间为起点，依次给出：简单空间本身、它的幂集、幂集上 Deng entropy
最大的 mass function、它的置换集（RPS）、以及置换集上 RPS entropy 最大的分布。

预期输出（`python -m example.space_example`，元素顺序每次运行可能不同）：:

    simple space of length=2:  {A, B}
    powerset of above set:  {{A, B}, {A}, {B}}
    maximum deng entropy distribution of length 2:  {{A, B}: 0.6, {A}: 0.2, {B}: 0.2}
    Permutation set of the above set: {(A, B), (B, A), (B,), (A,)}
    Power set of the above set: {{A, B}, {A}, {B}}
    Maximum RPS entropy distribution of length 2: {(A, B): 0.4, (B, A): 0.4, (B,): 0.1, (A,): 0.1}

`Element.__str__` 直接打印内部的值，所以集合与元组按原样显示，不带 `Element(...)`
包装。`set` 与 `dict` 的打印顺序取决于元素哈希，逐字对照输出时需按内容比较。
"""

from dstz.element.combination import simple_space, powerset
from dstz.element.permutation import permutation_set
from dstz.math.stat.distribution import max_deng_entropy_distribution, max_rps_entropy_distribution

# 长度 2 的简单空间，按 A、B 生成
ss = simple_space(2)
print('simple space of length=2: ', ss)

# 幂集默认不含空集
ps = powerset(ss)
print('powerset of above set: ', ps)

# 幂集上 Deng entropy 最大的分布：质量向多元集合倾斜
max_distributions = max_deng_entropy_distribution(2)
print('maximum deng entropy distribution of length 2: ', max_distributions)

# 置换集把每个子集展开成所有排列，(A, B) 与 (B, A) 是不同元素
per_s = permutation_set(ss)
print('Permutation set of the above set:', per_s)

# 与前面的幂集计算完全等价：重新算一次并覆盖 ps，保留原示例写法
ps = powerset(ss)
print('Power set of the above set:', ps)

# 在置换集上求 RPS entropy 最大的分布，质量在两种排列间均分
max_distributions = max_rps_entropy_distribution(2)
print('Maximum RPS entropy distribution of length 2:', max_distributions)
