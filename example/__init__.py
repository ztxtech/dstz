"""`example` 包：`dstz` 各项功能的最小可运行示例。

每个模块都是一个独立脚本，用 `python -m example.<模块名>` 运行；直接 `python
example/<模块名>.py` 时脚本所在目录成为 `sys.path` 首项而仓库根目录不在其中，`dstz`
会导入失败并报 `ModuleNotFoundError`。示例只做演示、不含断言，输出靠人工对照；涉及
`set`/`dict` 打印的模块，元素顺序会随 Python 的哈希种子变化。
"""
