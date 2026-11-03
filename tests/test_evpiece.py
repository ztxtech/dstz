"""证据变换与组合规则的测试。

组合规则用 `conftest.combine_reference` 按定义独立重算后对比，避免把实现的输出
直接当期望值；空集策略统一为"空集质量作为冲突，扣除后按 `1 - m(∅)` 归一化"，
完全冲突抛 `ValueError`。
"""

import pytest

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.dual import (conjunctive_rule, disjunctive_rule, ds_rule,
                               rps_left_rule, wang_orthogonal_rule)
from dstz.evpiece.single import (contour_transformation, get_fod,
                                 pignistic_probability_transformation,
                                 shafer_discounting, temperature_transformation)

from conftest import combine_reference, freeze


class TestBeliefFunctions:
    """`bel`/`pl`/`q` 在混合证据上的取值与空集约定。"""

    def test_values_on_mixed_evidence(self, element_evidence):
        """`bel` 只累加被包含的焦点元素，`pl` 累加相交的焦点元素。"""
        from dstz.math.func import bel, pl, q

        ev = element_evidence
        assert round(bel(Element({'A'}), ev), 12) == 0.2
        assert round(pl(Element({'A'}), ev), 12) == 0.5
        assert round(q(Element({'A'}), ev), 12) == 0.5
        assert round(bel(Element({'A', 'B'}), ev), 12) == 0.5
        assert round(pl(Element({'A', 'B'}), ev), 12) == 1.0
        assert round(q(Element({'A', 'B'}), ev), 12) == 0.3
        assert round(bel(Element({'B'}), ev), 12) == 0.0
        assert round(pl(Element({'B'}), ev), 12) == 0.8
        assert round(q(Element({'B'}), ev), 12) == 0.8

    def test_empty_set_convention(self, element_evidence):
        """`Bel(∅) = Pl(∅) = 0`，`Q(∅) = 1 - m(∅)`。"""
        from dstz.math.func import bel, pl, q

        empty = Element(set())
        assert round(bel(empty, element_evidence), 12) == 0.0
        assert round(pl(empty, element_evidence), 12) == 0.0
        assert round(q(empty, element_evidence), 12) == 1.0

    def test_commonality_ignores_empty_mass(self):
        """含空集质量时 `Q(∅)` 相应减少。"""
        from dstz.math.func import q

        ev = Evidence({Element(set()): 0.3, Element({'A'}): 0.7})
        assert round(q(Element(set()), ev), 12) == 0.7
        assert round(q(Element({'A'}), ev), 12) == 0.7


class TestDempsterShafer:
    """`ds_rule`：交运算 + 冲突扣除与归一化。"""

    def test_matches_reference(self, element_evidence):
        """两条证据的合成结果与按定义枚举的结果一致。"""
        ev2 = Evidence({Element({'A'}): 0.7, Element({'A', 'B'}): 0.3})
        got = ds_rule(element_evidence, ev2)
        want = combine_reference(element_evidence, ev2, set.intersection, True)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == want

    def test_fully_conflicting_raises(self):
        """完全冲突时无法用 `1 - m(∅)` 归一化，应当报错。"""
        ev1 = Evidence({Element({'A'}): 1.0})
        ev2 = Evidence({Element({'B'}): 1.0})
        with pytest.raises(ValueError):
            ds_rule(ev1, ev2)

    def test_empty_set_placeholders_are_conflict(self):
        """输入若带空集质量，它同样作为冲突参与扣除。"""
        ev1 = Evidence({Element(set()): 0.5, Element({'A'}): 0.5})
        ev2 = Evidence({Element({'A'}): 1.0})
        got = ds_rule(ev1, ev2)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            ('A',): 1.0}


class TestConjunctiveRule:
    """`conjunctive_rule`：只做交运算，空集质量保留在分布里。"""

    def test_matches_reference(self, element_evidence):
        """与按定义枚举的结果一致，空集不扣除。"""
        ev2 = Evidence({Element({'A'}): 0.7, Element({'A', 'B'}): 0.3})
        got = conjunctive_rule(element_evidence, ev2)
        want = combine_reference(element_evidence, ev2, set.intersection, False)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == want

    def test_full_conflict_kept(self):
        """完全冲突不报错，质量留在空集上。"""
        ev1 = Evidence({Element({'A'}): 1.0})
        ev2 = Evidence({Element({'B'}): 1.0})
        got = conjunctive_rule(ev1, ev2)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            (): 1.0}


class TestDisjunctiveRule:
    """`disjunctive_rule`：并运算，质量守恒且不归一化。"""

    def test_matches_reference(self, element_evidence):
        """与按定义枚举的结果一致。"""
        ev2 = Evidence({Element({'A'}): 0.7, Element({'A', 'B'}): 0.3})
        got = disjunctive_rule(element_evidence, ev2)
        want = combine_reference(element_evidence, ev2, set.union, False)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == want

    def test_mass_is_conserved(self):
        """并运算不会产生空集，总质量保持为 1。"""
        ev1 = Evidence({Element({'A'}): 0.5, Element({'B'}): 0.5})
        ev2 = Evidence({Element({'C'}): 1.0})
        got = disjunctive_rule(ev1, ev2)
        assert round(sum(got.values()), 12) == 1.0


class TestRPSLeftRule:
    """`rps_left_rule`：以左证据的顺序为准取有序交。"""

    def test_order_follows_left_evidence(self):
        """`(1, 3, 2)` 与 `(2, 3)` 的有序交为 `(3, 2)`。"""
        ev1 = Evidence({Element((1, 3, 2)): 1.0})
        ev2 = Evidence({Element((2, 3)): 1.0})
        got = rps_left_rule(ev1, ev2)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            (3, 2): 1.0}

    def test_duplicates_are_kept(self):
        """左侧的重复元素在有序交中保留。"""
        ev1 = Evidence({Element((1, 1, 2)): 1.0})
        ev2 = Evidence({Element((2,)): 1.0})
        got = rps_left_rule(ev1, ev2)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            (2,): 1.0}

    def test_empty_result_is_renormalized(self):
        """一侧含空排列时，空集质量被扣除后重新归一化。"""
        ev1 = Evidence({Element(()): 0.5, Element((1,)): 0.5})
        ev2 = Evidence({Element((1,)): 1.0})
        got = rps_left_rule(ev1, ev2)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            (1,): 1.0}

    def test_fully_conflicting_raises(self):
        """有序交全为空时视为完全冲突。"""
        ev1 = Evidence({Element((1, 2)): 1.0})
        ev2 = Evidence({Element((3,)): 1.0})
        with pytest.raises(ValueError):
            rps_left_rule(ev1, ev2)


class TestWangOrthogonalRule:
    """Wang 正交和（`order_code_intersection`）的数值回归。"""

    def test_regression_values(self):
        """与 `example/wang_orthogonal_example.py` 的预期输出一致。"""
        ev1 = Evidence({Element(('b', 'c')): 0.9, Element('a'): 0.1})
        ev2 = Evidence({Element(('c', 'a', 'b')): 0.4, Element('a'): 0.6})
        got = wang_orthogonal_rule(ev1, ev2)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            ('c', 'b'): 0.782608695652, ('a',): 0.217391304348}


class TestSingleEvidenceTransforms:
    """单证据变换：pignistic、折扣、contour、温度。"""

    def test_pignistic_probability_transformation(self):
        """`{A: 0.4, AB: 0.6}` 的 BetP 为 `{A: 0.7, B: 0.3}`。"""
        ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        got = pignistic_probability_transformation(ev)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            'A': 0.7, 'B': 0.3}

    def test_pignistic_rejects_empty_focal_element(self):
        """空焦元没有单元素可以分摊，应当报错。"""
        ev = Evidence({Element(set()): 0.5, Element({'A'}): 0.5})
        with pytest.raises(ValueError):
            pignistic_probability_transformation(ev)

    def test_shafer_discounting(self):
        """`alpha = 0.8` 时原证据打折、剩余质量交给辨识框架。"""
        ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        got = shafer_discounting(ev, 0.8, fod={'A', 'B'})
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            ('A',): 0.32, ('A', 'B'): 0.68}

    def test_shafer_discounting_infers_fod(self):
        """不显式给 `fod` 时从证据本身推断。"""
        ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        got = shafer_discounting(ev, 0.8)
        assert round(sum(got.values()), 12) == 1.0

    def test_shafer_discounting_rejects_out_of_range_alpha(self):
        """折扣系数必须落在 `[0, 1]`。"""
        ev = Evidence({Element({'A'}): 1.0})
        for alpha in (-0.1, 1.1):
            with pytest.raises(ValueError):
                shafer_discounting(ev, alpha)

    def test_contour_transformation_equals_pl(self):
        """轮廓函数就是单元素命题的似然度 `Pl({θ})`。"""
        from dstz.math.func import pl

        ev = Evidence({Element({'A'}): 0.2, Element({'A', 'B'}): 0.3,
                       Element({'B', 'C'}): 0.5})
        got = contour_transformation(ev)
        assert set(got.keys()) == {Element({'A'}), Element({'B'}), Element({'C'})}
        for key, mass in got.items():
            assert round(mass, 12) == round(pl(key, ev), 12)

    def test_temperature_transformation(self):
        """`t = 2` 削弱双元素命题：`{A: 0.5, AB: 0.5}` 得到 `{A: 0.75, AB: 0.25}`。"""
        ev = Evidence({Element({'A'}): 0.5, Element({'A', 'B'}): 0.5})
        got = temperature_transformation(ev, 2.0)
        assert {freeze(key.value): round(mass, 12) for key, mass in got.items()} == {
            ('A',): 0.75, ('A', 'B'): 0.25}

    def test_get_fod(self):
        """辨识框架是全部焦元的原子取并，返回裸标量集合。"""
        ev = Evidence({Element({'A'}): 0.2, Element({'B', 'C'}): 0.8})
        assert get_fod(ev) == {'A', 'B', 'C'}

    def test_get_fod_keeps_scalar_atom_whole(self):
        """标量型焦元按其整体算一个原子，不拆成字符。"""
        ev = Evidence({Element('AB'): 0.5, Element({'C'}): 0.5})
        assert get_fod(ev) == {'AB', 'C'}
