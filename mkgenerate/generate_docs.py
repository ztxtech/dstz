import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml


def load_or_create_config(config_path: Path) -> dict | None:
    """加载配置，如果不存在则创建模板并返回 None。"""
    if config_path.exists():
        print(f"从 '{config_path}' 加载配置...")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"配置文件 '{config_path}' 未找到。正在为您创建一个模板...")
        default_config = {
            "site_name": "My Project Docs",
            "site_description": "Documentation for the project.",
            "repo_url": "https://github.com/your_username/your_repo",
            "repo_name": "your_username/your_repo",
            "theme": {
                "name": "material",
                "palette": {"scheme": "default", "primary": "indigo", "accent": "indigo"},
                "font": {"text": "Roboto", "code": "Roboto Mono"},
                "features": [
                    "navigation.tabs", "navigation.sections", "toc.integrate",
                    "navigation.top", "search.suggest", "search.highlight",
                    "content.tabs.link"
                ]
            },
            # 新增字段，用于生成 requirements.txt
            "docs_requirements": [
                "mkdocs",
                "mkdocs-material",
                "mkdocstrings[python]",
                "pyyaml"
            ]
        }
        # 确保父目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        print(f"模板已创建。请填写 '{config_path}' 中的信息后重新运行脚本。")
        return None


def create_md_file(md_path: Path, package_name: str, py_path: Path, src_root: Path):
    """为 Python 文件创建对应的 Markdown 文件并填充 mkdocstrings 引用。"""
    relative_py_path = py_path.relative_to(src_root)
    module_path_parts = list(relative_py_path.parts)
    module_path_parts[-1] = module_path_parts[-1].replace('.py', '')
    if module_path_parts[-1] == '__init__':
        module_path_parts.pop()
    docstring_ref = f"{package_name}.{'.'.join(module_path_parts)}"
    if not module_path_parts:
        docstring_ref = package_name
    content = f"::: {docstring_ref}\n"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)


def build_nav_recursive(current_dir: Path, docs_root: Path) -> list:
    """递归构建导航结构。"""
    nav = []
    items = sorted(list(current_dir.iterdir()))
    index_file = current_dir / 'index.md'
    if index_file in items:
        title = current_dir.name.replace('_', ' ').capitalize() + " Overview"
        path = index_file.relative_to(docs_root).as_posix()
        nav.append({title: path})
        items.remove(index_file)
    for item in items:
        if item.is_dir():
            sub_nav = build_nav_recursive(item, docs_root)
            if sub_nav:
                nav.append({item.name.replace('_', ' ').capitalize(): sub_nav})
        elif item.is_file() and item.suffix == '.md':
            title = item.stem.replace('_', ' ').capitalize()
            path = item.relative_to(docs_root).as_posix()
            nav.append({title: path})
    return nav


def main():
    """主执行函数"""
    script_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description="(V5) 自动为 Python 软件包生成 MkDocs 文档结构。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("package_path", type=str, help="要为其生成文档的软件包的根目录路径。")
    parser.add_argument(
        "--config", type=str, default=script_dir / 'mkinfo.json',
        help="配置 (mkinfo.json) 文件的路径。\n默认: %(default)s"
    )
    parser.add_argument(
        "--readme", type=str, default=script_dir / 'readme.md',
        help="用作文档首页的 Markdown (readme.md) 文件的路径。\n默认: %(default)s"
    )
    parser.add_argument(
        "-o", "--output_dir", type=str, default=script_dir / 'out',
        help="生成文档结构的输出目录路径。\n默认: %(default)s"
    )

    args = parser.parse_args()

    # --- 1. 解析所有路径 ---
    config_path = Path(args.config)
    readme_path = Path(args.readme)
    src_path = Path(args.package_path)
    output_path = Path(args.output_dir)

    print("--- 路径配置 ---")
    print(f"源软件包: {src_path}")
    print(f"配置文件: {config_path}")
    print(f"首页文件: {readme_path}")
    print(f"输出目录: {output_path}")
    print("--------------------")

    # --- 2. 加载配置和检查源文件 ---
    config = load_or_create_config(config_path)
    if config is None:
        sys.exit(1)

    if not readme_path.exists():
        print(f"错误: 未在指定路径 '{readme_path}' 找到首页文件。")
        sys.exit(1)

    if not src_path.is_dir():
        print(f"错误: 提供的软件包路径 '{src_path}' 不是一个有效的目录。")
        sys.exit(1)

    # --- 3. 设置和创建目录 ---
    docs_path = output_path / "docs"
    api_docs_path = docs_path / "api"
    package_name = src_path.name

    if output_path.exists():
        shutil.rmtree(output_path)
    api_docs_path.mkdir(parents=True)
    shutil.copy(readme_path, docs_path / 'index.md')
    print("\n文档目录结构已创建，首页文件已复制。")

    # --- 4. 生成 requirements.txt ---
    requirements_list = config.get('docs_requirements', [])
    if requirements_list:
        requirements_path = docs_path / 'requirements.txt'
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements_list) + '\n')
        print("docs/requirements.txt 文件已生成。")

    # --- 5. 生成 API 文档 ---
    for py_file in src_path.rglob("*.py"):
        if "__pycache__" in py_file.parts: continue
        relative_path = py_file.relative_to(src_path)
        md_file = relative_path.with_suffix(
            '.md') if py_file.name != '__init__.py' else relative_path.parent / 'index.md'
        md_path = api_docs_path / md_file
        create_md_file(md_path, package_name, py_file, src_path)
    print("API Markdown 文件已生成。")

    # --- 6. 生成导航和 mkdocs.yml ---
    nav_structure = [{'Home': 'index.md'}]
    if api_docs_path.is_dir():
        api_nav = build_nav_recursive(api_docs_path, docs_path)
        if api_nav: nav_structure.append({'API Reference': api_nav})

    mkdocs_config = {
        'site_name': config['site_name'], 'site_description': config['site_description'],
        'repo_url': config['repo_url'], 'repo_name': config['repo_name'],
        'theme': config['theme'], 'nav': nav_structure,
        'plugins': [
            'search',
            {'mkdocstrings': {
                'handlers': {'python': {
                    'options': {'show_root_heading': True, 'show_source': True}
                }}
            }}
        ],
    }

    with open(output_path / 'mkdocs.yml', 'w', encoding='utf-8') as f:
        yaml.dump(mkdocs_config, f, sort_keys=False, default_flow_style=False, indent=2)
    print("mkdocs.yml 文件已生成。")

    print(f"\n🎉 成功! 文档骨架已在 '{output_path}' 目录中生成。")
    print("\n下一步:")
    print(f"1. 进入生成目录: cd \"{output_path}\"")
    print("2. （可选）安装依赖: pip install -r docs/requirements.txt")
    print("3. 启动本地开发服务器: mkdocs serve")


if __name__ == "__main__":
    main()
