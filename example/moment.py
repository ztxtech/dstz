"""`dstz.math.stat.moment` 中 Deng entropy 与信息方差的示例。

在 `{a, b, c}` 幂集的 7 个非空子集上平均分配质量（各 1/7），这种均匀分布给出该识别
框架下 Deng entropy 与信息方差的一组基准数值。

预期输出（`python -m example.moment`）：:

    entropy 3.8876752683749
    var 1.035416527115426
"""

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.math.stat.moment import deng_entropy, information_var

# 幂集 7 个非空子集等概率，便于对照解析结果
ev = {
    Element({'a'}): 1 / 7,
    Element({'b'}): 1 / 7,
    Element({'c'}): 1 / 7,
    Element({'a', 'b'}): 1 / 7,
    Element({'a', 'c'}): 1 / 7,
    Element({'b', 'c'}): 1 / 7,
    Element({'a', 'b', 'c'}): 1 / 7
}

# Evidence 构造时逐个校验键为 Item、值为 float，这里顺便把普通 dict 包装成 Evidence
ev = Evidence(ev)

# Deng entropy 度量命题集合的不确定性，information_var 度量质量的离散程度
d_entropy = deng_entropy(ev)
d_var = information_var(ev)

print('entropy', d_entropy)
print('var', d_var)
