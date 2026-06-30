from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    """向上查找包含 scripts/generate_problem.py 的仓库根目录。

    不再依赖 skill 相对仓库根的固定层级，便于 skill 目录迁移。
    """
    for candidate in (start, *start.parents):
        if (candidate / "scripts" / "generate_problem.py").is_file():
            return candidate
    raise FileNotFoundError(
        "找不到 scripts/generate_problem.py，请在 leetcode-practice 仓库内运行。"
    )


SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root(SKILL_DIR)
GENERATOR = REPO_ROOT / "scripts" / "generate_problem.py"


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    command = [sys.executable, str(GENERATOR), *args]
    completed = subprocess.run(command, cwd=REPO_ROOT)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
