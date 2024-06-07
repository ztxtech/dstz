from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="evidence_theory",
    version="0.0.1",
    author="Tianxiang Zhan",
    author_email="zhantianxianguestc@hotmail.com",  # 添加作者邮箱
    description="A python package of evidence theory",  # 添加项目描述
    long_description=long_description,  # 使用README.md的内容
    long_description_content_type="text/markdown",  # 指定README文件类型
    url="https://github.com/ztxtech/evidence_theory",  # 项目的URL
    packages=find_packages(),  # 自动查找所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 添加许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定Python版本要求
    #install_requires=["dependencies"],  # 如果有依赖项，替换为实际的依赖列表，如['numpy', 'pandas']
)