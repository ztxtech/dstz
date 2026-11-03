"""mass 函数上的高阶矩、Deng 熵与信息量。

这里把焦点元素的信息量 I(A) 当成随机变量、用 mass 作权重求各阶矩：一阶矩是 Deng
熵，二阶中心矩是 `information_var`。注意这些矩都不再除以总质量，按 `Evidence` 之和
为 1 的约定使用才是通常意义下的期望与方差。
"""

import math

from dstz.core.atom import atom_set
from dstz.element.combination import powerset


def high_order_moment(ev, func, order, *args):
    """计算以 mass 为权重的广义 `order` 阶矩。

        E[f ** order] = Σ_{A} m(A) * f(A, m(A), *args) ** order

    `func` 的签名必须与 `(element, mass, *args)` 一致：每次求值都会把焦点元素和它
    自己的质量一起传进去，所以 `func` 既可以是原始信息量，也可以是中心化后的量。

    Args:
        ev (Evidence): mass 函数，键为焦点元素。
        func (callable): 取值函数，签名为 `func(element, mass, *args)`，返回数值。
        order (int): 矩的阶数。
        *args: 原样转发给 `func` 的额外参数。

    Returns:
        float: 各焦点元素 `func` 取值的加权幂和；`ev` 为空时返回整数 `0`（累加
        初始值），否则返回累加结果的类型。
    """
    res = 0
    for element, mass in ev.items():
        res += (func(element, mass, *args) ** order) * mass
    return res


def deng_entropy(ev):
    """计算 mass 函数的 Deng 熵。

        E_d = Σ_{A} m(A) * log2((2 ** |A| - 1) / m(A))

    即焦点元素信息量 `information_content` 的一阶矩，用 mass 作权重取期望。

    Args:
        ev (Evidence): mass 函数。

    Returns:
        float: Deng 熵，单位为 bit；`ev` 为空时返回整数 `0`（累加初始值）。

    Raises:
        ValueError: 某个焦点元素的质量不为正，或焦点元素为空集（内部状态数为 0）
            时，`information_content` 抛出的异常会原样传上来。
    """
    return high_order_moment(ev, information_content, 1)


def information_var(ev):
    """计算信息量的二阶中心矩。

        Var = Σ_{A} m(A) * (I(A) - E_d) ** 2

    其中 `E_d` 是 Deng 熵。得到的矩不再除以总质量 Σ m(A)，只有输入本身是归一化的
    mass 函数时才等同于通常意义下的方差。

    Args:
        ev (Evidence): mass 函数。

    Returns:
        float: 信息量的二阶中心矩，单位为 bit²；`ev` 为空时返回整数 `0`（累加
        初始值）。

    Raises:
        ValueError: 质量不为正或焦点元素为空集时，`information_content` 抛出的
            异常会原样传上来。
    """
    return high_order_moment(ev, central_information_content, 2, ev)


def information_content(element, mass, event_generator=powerset,
                        component_generator=set):
    """计算单个焦点元素的信息量。

        I(A) = -log2(m(A) / N(A)),
        其中 N(A) = len(event_generator(component_generator(A)))

    默认参数下 `N(A) = 2 ** |A| - 1`（非空子集个数），即 Deng 熵采用的信息量定义：
    焦距越大、质量越小，信息量越大。

    Args:
        element (Element): 焦点元素。
        mass (float): 该元素的质量，必须为正。
        event_generator (callable): 把元素集合展开成"内部状态"的生成器，默认
            `powerset`。
        component_generator (callable): 把原子集合规整成集合，默认 `set`；处理
            排列型元素时它起去掉顺序与重复的作用。

    Returns:
        float: 信息量，单位为 bit。

    Raises:
        ValueError: `mass <= 0`，或 `element` 的内部状态数为 0（空集焦点元素）时
            没有定义信息量，直接抛出并指明是哪种情况。

    Note:
        `element.value` 是标量时按单原子焦点元素处理，`N = 2 ** 1 - 1 = 1`，因此
        对贝叶斯 mass 函数（全部为单元素命题）`deng_entropy` 退化为香农熵。
    """
    if mass <= 0:
        raise ValueError(f"焦点元素 {element} 的质量必须为正，实际为 {mass}")
    states = len(event_generator(component_generator(atom_set(element.value))))
    if states == 0:
        raise ValueError(
            f"焦点元素 {element} 的内部状态数为 0（空集占位），信息量无定义")
    return -math.log2(mass / states)


def central_information_content(element, mass, ev):
    """计算焦点元素信息量相对整个分布的偏离量。

        ΔI(A) = I(A) - E_d

    减去的 `E_d` 是整条 mass 函数的 Deng 熵，即平均信息量。结果为正表示该元素比
    平均水平更"意外"。

    Args:
        element (Element): 焦点元素。
        mass (float): 该元素的质量。
        ev (Evidence): 用来计算平均信息量的整条 mass 函数。

    Returns:
        float: 中心化后的信息量，单位为 bit。

    Raises:
        ValueError: `mass` 或 `ev` 中某个质量不为正、或其中任一焦点元素为空集时，
            由 `information_content` 抛出。

    Note:
        每次调用都重新算一遍 `ev` 的平均信息量，所以 `information_var` 的整体代价
        是 O(n²)。
    """
    center = high_order_moment(ev, information_content, 1)
    return information_content(element, mass) - center