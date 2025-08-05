# dstz

![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-green)
[![Python](https://img.shields.io/badge/PyPI-3670A0?logo=PyPI&logoColor=ffdd54)](https://pypi.org/project/dstz/)
[![Python Version](https://img.shields.io/badge/python-%3E%3D3.7-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repository](https://img.shields.io/badge/repository-GitHub-blue.svg)](https://github.com/ztxtech/dstz)
[![GitHub Issues](https://img.shields.io/github/issues/ztxtech/dstz.svg)](https://github.com/ztxtech/dstz/issues)
[![Documentation Status](https://readthedocs.org/projects/dst/badge/?version=latest)](https://dst.readthedocs.io/en/latest/?badge=latest)

## 简介

`dstz`是一个用于证据理论的Python包，提供了一系列工具和函数，帮助用户处理和应用证据理论。

## 安装

使用`pip`安装`dstz`:

```bash
pip install dstz
```

## 例子

- 见[`./example/conflict_example.py`](https://github.com/ztxtech/dstz/blob/main/example/conflict_example.py)
  中实现了一个经典的证据冲突的融合。
- 见[`./example/ppt.py`](https://github.com/ztxtech/dstz/blob/main/example/ppt.py)
  中实现了一个pignistic probability transformation。
- 见[`./example/moment.py`](https://github.com/ztxtech/dstz/blob/main/example/moment.py)
  中实现了一个计算证据对应的矩的例子。
- 见[`./example/space_example.py`](https://github.com/ztxtech/dstz/blob/main/example/space_example.py)
  中实现了一个计算证据对应的矩的例子。
- 见[`./example/rps_example.py`](https://github.com/ztxtech/dstz/blob/main/example/rps_example.py)
  中实现了随机排列集左交融合的例子。
- 见[`./example/wang_orthogonal_example.py`](https://github.com/ztxtech/dstz/blob/main/example/wang_orthogonal_example.py)
中实现了论文[`Wang, Y., Li, Z., & Deng, Y. (2024). A new orthogonal sum in Random Permutation Set. Fuzzy Sets and Systems, 109034`](https://doi.org/10.1016/j.fss.2024.109034)
中的正交rps融合规则。

## 文档

完整的[API文档](https://dstz.readthedocs.io/)和使用指南可在项目主页上找到。

## 支持与交流

有任何问题或建议，欢迎在GitHub Issues页面提交。

## 许可证

本项目遵循[MIT License](https://opensource.org/licenses/MIT)。

作者：Tianxiang Zhan 电子邮件：[zhantianxianguestc@hotmail.com](mailto:zhantianxianguestc@hotmail.com)

## 致谢

感谢所有贡献者和社区成员的帮助和支持。

## 相关论文

本软件包的编程思想基于Zhan等人的论文，如果涉及相关内容，请引用相关文献。

```bibtex
@article{zhan2024generalized,
  title={Generalized information entropy and generalized information dimension},
  author={Zhan, Tianxiang and Zhou, Jiefeng and Li, Zhen and Deng, Yong},
  journal={Chaos, Solitons \& Fractals},
  volume={184},
  pages={114976},
  year={2024},
  publisher={Elsevier}
}
```

```bibtex
@article{zhan2024random,
  title={Random Graph Set and Evidence Pattern Reasoning Model},
  author={Zhan, Tianxiang and Li, Zhen and Deng, Yong},
  journal={arXiv preprint arXiv:2402.13058},
  year={2024}
}
```
