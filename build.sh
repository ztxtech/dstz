#!/bin/bash
# build.sh - 本地打包预检：清理 -> 构建 sdist/wheel -> 校验元数据，不上传。
#
# 正式发布不在这里做：推送 vX.Y.Z 标签即可触发 .github/workflows/publish.yml，
# 由 GitHub Actions 用 PyPI trusted publishing（OIDC）上传，
# 因此本地不需要、也不应该配置 PyPI token。详见 README「发布」一节。

set -euo pipefail

cd "$(dirname "$0")"

sh ./clean.sh
python -m build
python -m twine check --strict dist/*

echo "预检完成：dist/ 下的发行包已生成并通过元数据校验，可推送标签触发发布。"
