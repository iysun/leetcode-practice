from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[1]
GENERATOR = REPO_ROOT / "scripts" / "generate_problem.py"


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    command = [sys.executable, str(GENERATOR), *args]
    completed = subprocess.run(command, cwd=REPO_ROOT)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
