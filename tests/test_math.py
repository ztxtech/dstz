"""`dstz.math` 下统计量与矩阵规则的测试。

两类断言各自解决一个风险：Deng 熵与信息量的期望必须有闭式解可对照，矩阵规则必须
与 `dstz.evpiece.dual` 的逐项实现给出同一个分布，否则两条代码路径会在冲突处理和
归一化上悄悄分叉。
"""

import math

import pytest

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.element.combination import simple_space
from dstz.evpiece.dual import conjunctive_rule, disjunctive_rule
from dstz.math.matrix.const import get_bfrm, get_qfrm, matrix_self_kron
from dstz.math.matrix.dual import (
    conjunctive_rule as matrix_conjunctive_rule,
    de_conjunctive_rule,
    de_disjunctive_rule,
    disjunctive_rule as matrix_disjunctive_rule,
)
from dstz.math.stat.distribution import (
    max_deng_entropy_distribution,
    max_rps_entropy_distribution,
)
from dstz.math.stat.moment import deng_entropy, information_content, information_var

from conftest import norm_ev

class TestDengEntropy:
    """Deng 熵：一阶信息量矩，最大熵分布有已知闭式解。"""

    def test_max_entropy_distribution_matches_closed_form(self):
        """`n = 3` 的最大 Deng 熵分布，其熵恰为 `log2(19)`。

        该分布由 `max_deng_entropy_distribution` 的构造给出：`2**n - 1` 个非空
        焦元按 `2^{|A|} - 1` 的比例分配质量，熵收敛到 `log2(2 ** (n + 1) - 1)`。
        """
        ev = max_deng_entropy_distribution(3)
        assert deng_entropy(ev) == pytest.approx(math.log2(19), rel=1e-12)

    def test_max_entropy_two_atoms(self):
        """`n = 2` 时闭式解是 `log2(5)`，与一阶矩定义一致。"""
        assert deng_entropy(max_deng_entropy_distribution(2)) == pytest.approx(
            math.log2(5), rel=1e-12)

    def test_bayesian_evidence_degenerates_to_shannon(self):
        """单元素焦元占满时，Deng 熵退化为 Shannon 熵。

        此时 `|A| = 1`、信息量 `I(A) = -log2 m(A)`，故 `H = -Σ m log2 m`；这里
        `0.5/0.25/0.25` 的 Shannon 熵为 1.5 bit。
        """
        ev = Evidence({
            Element({'A'}): 0.5,
            Element({'B'}): 0.25,
            Element({'C'}): 0.25,
        })
        assert deng_entropy(ev) == pytest.approx(1.5, rel=1e-12)

class TestInformationContent:
    """焦点元素的信息量与信息量方差。"""

    def test_singleton_information_content(self):
        """单元素焦元的信息量是 `-log2 m`。"""
        assert information_content(Element({'A'}), 0.5) == pytest.approx(1.0)

    def test_uniform_max_entropy_has_zero_variance(self):
        """最大熵分布的每个焦元信息量相同，故信息量方差为 0。"""
        assert information_var(max_deng_entropy_distribution(3)) == pytest.approx(0.0)

    def test_rps_max_entropy_distribution(self):
        """`n = 2` 的 RPS 最大熵分布把质量按 `0.1/0.1/0.4/0.4` 分配。

        分母是排列数：长度 1 的两条排列各占 `1/10`，长度 2 的两条各占 `4/10`。
        """
        ev = max_rps_entropy_distribution(2)
        assert norm_ev(ev) == {
            ('A',): 0.1,
            ('B',): 0.1,
            ('A', 'B'): 0.4,
            ('B', 'A'): 0.4,
        }
        assert deng_entropy(ev) == pytest.approx(2.9898980954642878, rel=1e-12)

class TestMatrixRules:
    """矩阵规则与逐项实现必须给出同一个分布。"""

    @pytest.fixture(name="pair")
    def fixture_pair(self):
        """两条共享 `{A}`、`{A, B}` 结构的证据。"""
        ev1 = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        ev2 = Evidence({Element({'A'}): 0.7, Element({'A', 'B'}): 0.3})
        return ev1, ev2

    def test_conjunctive_matches_pointwise(self, pair):
        """合取规则：矩阵实现 `{A: 0.82, AB: 0.18}` 与逐项实现一致。"""
        ev1, ev2 = pair
        assert norm_ev(matrix_conjunctive_rule(ev1, ev2)) == norm_ev(
            conjunctive_rule(ev1, ev2))
        assert norm_ev(matrix_conjunctive_rule(ev1, ev2)) == {
            ('A',): 0.82,
            ('A', 'B'): 0.18,
        }

    def test_disjunctive_matches_pointwise(self, pair):
        """析取规则：矩阵实现 `{A: 0.28, AB: 0.72}` 与逐项实现一致。"""
        ev1, ev2 = pair
        assert norm_ev(matrix_disjunctive_rule(ev1, ev2)) == norm_ev(
            disjunctive_rule(ev1, ev2))
        assert norm_ev(matrix_disjunctive_rule(ev1, ev2)) == {
            ('A',): 0.28,
            ('A', 'B'): 0.72,
        }

    def test_de_conjunctive_recovers_operand(self, pair):
        """逆合取从合成结果与另一条证据恢复出原证据。"""
        ev1, ev2 = pair
        assert norm_ev(de_conjunctive_rule(matrix_conjunctive_rule(ev1, ev2), ev2)) == \
            norm_ev(ev1)

    def test_de_disjunctive_recovers_operand(self, pair):
        """逆析取同样能恢复原证据。"""
        ev1, ev2 = pair
        assert norm_ev(de_disjunctive_rule(matrix_disjunctive_rule(ev1, ev2), ev2)) == \
            norm_ev(ev1)

    def test_full_conflict_stays_on_empty_set(self):
        """矩阵实现刻意不重归一化，完全冲突时质量整块留在空集上。"""
        ev1 = Evidence({Element({'A'}): 1.0})
        ev2 = Evidence({Element({'B'}): 1.0})
        got = matrix_conjunctive_rule(ev1, ev2)
        assert norm_ev(got) == {(): 1.0}

class TestBeliefFunctionsOnAtoms:
    """标量原子（`simple_space` 的产物）与集合焦元走同一套判据。"""

    @pytest.fixture(name="scalar_evidence")
    def fixture_scalar_evidence(self):
        """键为集合焦元、查询用 `simple_space` 的标量原子的证据。"""
        ev = Evidence({Element({'A'}): 0.4, Element({'A', 'B'}): 0.6})
        atom = next(item for item in simple_space(26) if item.value == 'A')
        return ev, atom

    def test_scalar_atom_matches_singleton_set(self, scalar_evidence):
        """`Element('A')` 与 `Element({'A'})` 给出相同的 Bel/Pl/Q。"""
        from dstz.math.func import bel, pl, q

        ev, atom = scalar_evidence
        singleton = Element({'A'})
        assert round(bel(atom, ev), 12) == round(bel(singleton, ev), 12) == 0.4
        assert round(pl(atom, ev), 12) == round(pl(singleton, ev), 12) == 1.0
        assert round(q(atom, ev), 12) == round(q(singleton, ev), 12) == 1.0


class TestMatrixConstants:
    """基础矩阵的形状约定。"""

    def test_empty_fod_matrices_are_one_by_one(self):
        """`n = 0` 的 BFRM/QFRM 都是 `1x1`，对应只有空集的平凡框架。"""
        assert get_bfrm(0).shape == (1, 1)
        assert get_qfrm(0).shape == (1, 1)

    def test_self_kron_grows_exponentially(self):
        """`1x1` 的 QFRM 做 3 次自 Kronecker 积得到 `8x8`。"""
        assert matrix_self_kron(get_qfrm(1), 3).shape == (8, 8)
