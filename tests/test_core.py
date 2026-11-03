"""核心数据结构与集合构造的测试。

覆盖 `Element` 的取值语义、`Evidence` 的类型校验，以及 `simple_space`、
`powerset`、`permutation_set` 两级代数约定：原子的 `value` 是标量，焦点元素的
`value` 是"原始标量组成的集合/元组"，不能在焦点元素里再嵌一层 `Element`。
"""

import pytest

from dstz.core.atom import Element, Item
from dstz.core.distribution import Evidence
from dstz.element.combination import powerset, simple_space
from dstz.element.permutation import (left_intersection, order_code_intersection,
                                      permutation_set)

from conftest import freeze


class TestElement:
    """`Element` 的基本行为。"""

    def test_value_kept_verbatim(self):
        """`value` 原样保存，`str`/`repr` 直接返回它的字符串形式。"""
        assert Element({'A', 'B'}).value == {'A', 'B'}
        assert str(Element('A')) == 'A'
        assert repr(Element(('A', 'B'))) == "('A', 'B')"

    def test_equality_and_hashing_follow_value(self):
        """相等性与哈希只看 `value`，因此可直接作为字典键。"""
        assert Element({'A', 'B'}) == Element({'A', 'B'})
        assert hash(Element({'A', 'B'})) == hash(Element({'A', 'B'}))
        assert len({Element({'A'}), Element({'A'})}) == 1

    def test_len_and_iteration(self):
        """`len` 与迭代作用于集合/元组取值；标量取值不参与迭代。"""
        assert len(Element({'A', 'B'})) == 2
        assert sorted(Element({'A', 'B'})) == ['A', 'B']
        assert tuple(Element(('B', 'A'))) == ('B', 'A')
        assert len(Element('A')) == 1
        assert list(Element('A')) == []

    def test_is_item(self):
        """`Element` 是 `Item` 的实现，`Evidence` 的键校验依赖这一点。"""
        assert isinstance(Element('A'), Item)


class TestEvidence:
    """`Evidence` 的类型校验边界。"""

    def test_rejects_non_item_key(self):
        """键必须是 `Item` 实例。"""
        with pytest.raises(TypeError):
            Evidence({'A': 0.5})

    def test_rejects_int_mass(self):
        """质量必须是 `float`，整数 `1` 也不接受。"""
        with pytest.raises(TypeError):
            Evidence({Element('A'): 1})

    def test_mass_range_is_not_enforced(self):
        """`Evidence` 只约束类型，不检查负值与总质量是否超过 1。

        归一化是组合规则的职责：`ds_rule` 等会按 `1 - m(∅)` 重归一化，因此容器
        层不做越界拦截。这里显式钉住该契约，避免后来者误以为构造器会报错。
        """
        negative = Evidence({Element('A'): -0.1})
        assert norm_like(negative) == {'A': -0.1}
        overloaded = Evidence({Element('A'): 0.7, Element('B'): 0.6})
        assert norm_like(overloaded) == {'A': 0.7, 'B': 0.6}

    def test_setitem_validates(self):
        """下标赋值同样做校验，非法值不会被写入。"""
        ev = Evidence()
        ev[Element('A')] = 0.5
        assert norm_like(ev) == {'A': 0.5}
        with pytest.raises(TypeError):
            ev[Element('B')] = 1

    def test_copy_returns_plain_dict(self):
        """`copy()` 返回普通 `dict`，这是已知且有文档说明的边界。"""
        ev = Evidence({Element('A'): 1.0})
        assert type(ev.copy()) is dict


def norm_like(ev):
    """把质量字典按 `freeze` 规整，方便与其他模块的断言共用同一比较口径。"""
    return {freeze(key.value): round(float(mass), 12) for key, mass in ev.items()}


class TestSimpleSpace:
    """`simple_space` 产出的是原子，`value` 为标量字符串。"""

    def test_atoms_are_scalars(self):
        """长度为 2 的辨识框架给出 `{'A', 'B'}`，且取值为标量。"""
        space = simple_space(2)
        assert {element.value for element in space} == {'A', 'B'}
        assert all(isinstance(element.value, str) for element in space)

    def test_zero_length_is_empty(self):
        """`simple_space` 不校验长度，`n <= 0` 只是给出空集合。"""
        assert simple_space(0) == set()
        assert simple_space(-3) == set()


class TestPowerset:
    """`powerset` 产出焦点元素，`value` 是原始标量组成的 `set`。"""

    def test_contains_non_empty_subsets(self):
        """默认不含空集，长度 2 的框架给出 3 个焦点元素。"""
        space = powerset(simple_space(2))
        assert {freeze(element.value) for element in space} == {
            ('A',), ('B',), ('A', 'B')}

    def test_allow_empty(self):
        """显式允许空集时多出空集这一项。"""
        space = powerset(simple_space(2), allow_empty=True)
        assert len(space) == 4

    def test_no_double_wrapping(self):
        """焦点元素内部装的是原始标量，不能再嵌一层 `Element`。"""
        for element in powerset(simple_space(3)):
            assert isinstance(element.value, set)
            assert all(not isinstance(atom, Element) for atom in element.value)

    def test_accepts_raw_collection(self):
        """传入普通集合时按原子集合处理，不要求先包成 `Element`。"""
        assert len(powerset({'A', 'B'})) == 3


class TestPermutationSet:
    """`permutation_set` 产出排列型焦点元素，`value` 是标量组成的 `tuple`。"""

    def test_count_and_order(self):
        """长度 2 的框架给出 4 条排列，顺序保留在元组里。"""
        space = permutation_set(simple_space(2))
        assert {freeze(element.value) for element in space} == {
            ('A',), ('B',), ('A', 'B'), ('B', 'A')}

    def test_no_double_wrapping(self):
        """排列里装的是原始标量。"""
        for element in permutation_set(simple_space(2)):
            assert isinstance(element.value, tuple)
            assert all(not isinstance(atom, Element) for atom in element.value)


class TestLeftIntersection:
    """`left_intersection` 保留左操作数的顺序与重复。"""

    def test_keeps_left_order_and_duplicates(self):
        """`(1, 3, 2) ←- (2, 3)` 取左侧顺序下的公共元素 `(3, 2)`。"""
        assert left_intersection((1, 3, 2), (2, 3)) == (3, 2)

    def test_keeps_duplicates(self):
        """重复出现在左侧时保留重复，`(1, 1, 2) ←- (2,)` 得到 `(2,)`。"""
        assert left_intersection((1, 1, 2), (2,)) == (2,)

    def test_left_empty(self):
        """左操作数为空排列时结果为空。"""
        assert left_intersection((), (1, 2)) == ()

    def test_disjoint(self):
        """无公共元素时结果为空。"""
        assert left_intersection((1, 2), (3, 4)) == ()


class TestOrderCodeIntersection:
    """`order_code_intersection` 是 Wang 正交规则用的有序交，行为固定不改。"""

    def test_simple_common_elements(self):
        """公共元素按位置键升序成组，再做笛卡尔积。"""
        assert order_code_intersection(('b', 'c'), ('c', 'a', 'b')) == [('c', 'b')]

    def test_disjoint_gives_empty_tuple(self):
        """没有公共元素时结果为单个空元组。"""
        assert order_code_intersection(('b',), ('a',)) == [()]
