"""把 Python 包的全部源码导出到一个纯文本文件。

用途是把一个包（例如 `dstz`）的目录结构和所有 `.py` 内容打包成单文件，方便
提交给评审或粘贴到对话里。命令行入口为 `python p2txt.py <包路径> <输出文件>`，
也可以直接调用 `export_package_code_to_txt`。
"""

import argparse
import glob
import os
import shutil


def export_package_code_to_txt(package_path, output_file):
    """把指定包的全部 `.py` 代码导出到单个文本文件。

    输出文件由三部分组成：一行 `--- Package Tree ---` 标题、`write_tree_structure`
    生成的目录树、以及逐文件拼接的源码；每个文件前加一行 `--- <相对路径> ---`
    作为分隔，文件内容之后补两个空行。

    几个实际行为：输出文件所在目录不存在时会用 `os.makedirs` 递归创建；包内文件按
    路径排序后写出，同一目录多次运行的输出顺序一致；相对路径由 `os.path.relpath`
    给出，在 Windows 上带反斜杠。

    Args:
        package_path (str): 包目录路径，会先转成绝对路径再参与比较与相对路径计算。
        output_file (str): 输出文本文件路径；只有文件名（例如 `out.txt`）时写到当前
            工作目录。

    Raises:
        OSError: 创建目录或读写文件因权限、路径非法等原因失败时由标准库抛出。

    Example:
        >>> export_package_code_to_txt('dstz/core', '/tmp/dstz-core.txt')
    """
    # 输出目录不存在时先创建，允许中间层级一起建；只有文件名时 dirname 为空串，
    # 表示就是当前目录，不需要创建
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 统一成绝对路径，后面算相对路径时才不会被当前目录影响
    package_path = os.path.abspath(package_path)

    # 递归收集包内所有 .py 文件
    python_files = glob.glob(os.path.join(package_path, '**', '*.py'), recursive=True)
    python_files.sort()  # 固定输出顺序，便于比较两次导出结果

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 先写目录树，再写代码
        outfile.write("--- Package Tree ---\n")
        write_tree_structure(package_path, outfile)
        outfile.write("\n\n")

        for file_path in python_files:
            # 逐个文件把内容原样拷进输出文件
            with open(file_path, 'r', encoding='utf-8') as infile:
                # 相对路径只用于标注来源，不参与读取
                relative_path = os.path.relpath(file_path, package_path)
                outfile.write(f"--- {relative_path} ---\n")
                shutil.copyfileobj(infile, outfile)
                # 空行让相邻文件的内容不粘连
                outfile.write("\n\n")


def write_tree_structure(package_path, outfile):
    """把包的目录结构写进给定的文件对象。

    目录集合来自每个 `.py` 文件所在目录及其所有上级目录，去掉代表根目录的空串后
    排序；随后把“目录 + 文件”合并成一个列表，按相对路径字符串统一排序再输出，因此
    同一层级里目录和文件是按名字混排的，而不是目录优先。

    缩进按路径层深计算（每层一个 `│   `），所有条目都用 `├── ` 前缀——末项没有换成
    `└──`，目录只在名字后多一个 `/`。所以这里的树只保证层级和顺序，不是严格的
    图形化树。

    Args:
        package_path (str): 包目录路径；用它的 `basename` 作为树根输出，不加分隔符
            就写入时会原样使用。
        outfile (TextIO): 已打开的可写文本文件对象，函数只往里写，不负责打开和关闭。

    Example:
        >>> with open('/tmp/tree.txt', 'w', encoding='utf-8') as f:
        ...     write_tree_structure('dstz/core', f)
    """
    # 收集全部 .py 文件；排序只为固定输出顺序，最终顺序由 all_items 排序决定
    python_files = glob.glob(os.path.join(package_path, '**', '*.py'), recursive=True)
    python_files.sort()

    # 目录集合：每个文件所在目录以及它的所有上级
    dirs = set()
    for file_path in python_files:
        relative_dir = os.path.dirname(os.path.relpath(file_path, package_path))
        dirs.add(relative_dir)
        while relative_dir:
            relative_dir = os.path.dirname(relative_dir)
            dirs.add(relative_dir)

    # 空串代表根目录，根目录单独输出，从集合里去掉
    dirs.discard('')

    sorted_dirs = sorted(dirs)

    # 树根：包目录名加斜杠
    outfile.write(f"{os.path.basename(package_path)}/\n")

    all_items = []
    for dir_path in sorted_dirs:
        all_items.append((dir_path, True))  # 目录

    for file_path in python_files:
        relative_path = os.path.relpath(file_path, package_path)
        all_items.append((relative_path, False))  # 文件

    # 目录和文件放在一起按相对路径排序
    all_items.sort(key=lambda x: x[0])

    for item_path, is_dir in all_items:
        parts = item_path.split(os.sep)
        indent = "│   " * (len(parts) - 1)

        if is_dir:
            outfile.write(f"{indent}├── {parts[-1]}/\n")
        else:
            outfile.write(f"{indent}├── {parts[-1]}\n")


def main():
    """命令行入口：解析两个位置参数并执行导出，成功时打印提示。

    参数说明由 `argparse` 提供，`--help` 的输出即用户可见的 CLI 文案。
    """
    parser = argparse.ArgumentParser(description="Export all Python code from a package to a text file.")
    parser.add_argument("package_path", help="Path to the Python package.")
    parser.add_argument("output_file", help="Path to the output text file.")

    args = parser.parse_args()

    export_package_code_to_txt(args.package_path, args.output_file)
    print("Export completed.")


if __name__ == "__main__":
    main()
