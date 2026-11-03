# dstz

![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-green)
[![Python](https://img.shields.io/badge/PyPI-3670A0?logo=PyPI&logoColor=ffdd54)](https://pypi.org/project/dstz/)
[![Python Version](https://img.shields.io/badge/python-%3E%3D3.9-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repository](https://img.shields.io/badge/repository-GitHub-blue.svg)](https://github.com/ztxtech/dstz)
[![GitHub Issues](https://img.shields.io/github/issues/ztxtech/dstz.svg)](https://github.com/ztxtech/dstz/issues)
[![Documentation Status](https://readthedocs.org/projects/dstz/badge/?version=latest)](https://dstz.readthedocs.io/en/latest/?badge=latest)

## 简介

`dstz`是一个用于证据理论的Python包，提供了一系列工具和函数，帮助用户处理和应用证据理论。

## 安装

使用`pip`安装`dstz`:

```bash
pip install dstz
```

要求 Python >= 3.9。

## 例子

仓库中的示例脚本用模块方式运行，例如：

```bash
git clone https://github.com/ztxtech/dstz.git
cd dstz
pip install -e .
python -m example.space_example
```

直接运行 `python example/space_example.py` 会因为包路径不在 `sys.path` 上而报 `ModuleNotFoundError`，请始终用 `python -m example.<脚本名>`。

- 见[`./example/conflict_example.py`](https://github.com/ztxtech/dstz/blob/main/example/conflict_example.py)
  中实现了一个经典的证据冲突的融合。
- 见[`./example/ppt.py`](https://github.com/ztxtech/dstz/blob/main/example/ppt.py)
  中实现了一个pignistic probability transformation。
- 见[`./example/moment.py`](https://github.com/ztxtech/dstz/blob/main/example/moment.py)
  中实现了一个计算证据对应的矩的例子。
- 见[`./example/space_example.py`](https://github.com/ztxtech/dstz/blob/main/example/space_example.py)
  中实现了辨识框架的幂集与排列集构造，以及对应的最大熵分布。
- 见[`./example/rps_example.py`](https://github.com/ztxtech/dstz/blob/main/example/rps_example.py)
  中实现了随机排列集左交融合的例子。
- 见[`./example/wang_orthogonal_example.py`](https://github.com/ztxtech/dstz/blob/main/example/wang_orthogonal_example.py)
中实现了论文[`Wang, Y., Li, Z., & Deng, Y. (2024). A new orthogonal sum in Random Permutation Set. Fuzzy Sets and Systems, 109034`](https://doi.org/10.1016/j.fss.2024.109034)
中的正交rps融合规则。

## 文档

完整的[API文档](https://dstz.readthedocs.io/)和使用指南可在项目主页上找到。

## 发布

发行包从 GitHub 直接发布到 PyPI，本地与仓库都不保存 PyPI token，鉴权使用 PyPI 的 trusted publishing（OIDC 短期令牌）：

1. 一次性配置（在 PyPI 完成）：在 dstz 项目的 Publishing settings 里添加 pending publisher，
   指定仓库 `ztxtech/dstz`、工作流 `publish.yml`、environment `pypi`；
   TestPyPI 同理，环境名为 `testpypi`。GitHub 侧在仓库 Settings → Environments
   创建同名 environment（可按需要加审批人）。
2. 本地预检（可选）：`sh ./build.sh`，只做清理、打包和 `twine check --strict`，不上传。
3. 正式发布：把 `pyproject.toml` 里的 `version` 改成目标版本号并提交，
   然后打标签推送：

   ```bash
   git tag v0.0.8
   git push origin v0.0.8
   ```

   CI 会先校验标签与 `pyproject.toml` 版本一致，再构建、校验并发布到 PyPI。
4. 想先演练整条链路：在 Actions 里手动运行 `publish` 工作流，`target` 选
   `testpypi`，产物投递到 TestPyPI。

每次推送标签都会同时构建 sdist 与 wheel；PR 与推送到 main 的提交由 `ci` 工作流跑测试并校验发行包。

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
