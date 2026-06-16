# leetcode-practice

用于把 LeetCode 题目同步到本地，并生成单文件模板。每道题每种语言只生成一个文件，文件里同时包含示例代码和测试代码，用注释分区隔开。

## 说明

目前支持两种语言：

- `solutions/py/`: Python 单文件模板
- `solutions/go/`: Go 单文件模板

同时会在 `problems/` 下保存一份精简题面元数据，包含标题、链接、签名、示例和约束。

## 使用

这个项目支持两种使用方式：

1. 直接运行脚本
2. 通过仓库内的 skill 让 agent 生成并复查题目

### 方式一：直接运行脚本

生成一道题：

```bash
python scripts/generate_problem.py 1
```

只生成 Python：

```bash
python scripts/generate_problem.py 1 --lang py
```

覆盖已存在文件：

```bash
python scripts/generate_problem.py 1 --force
```

生成结果示例：

- `solutions/py/0001_two_sum.py`
- `solutions/go/0001_two_sum.go`
- `problems/0001_two_sum.json`

### 方式二：使用 skill

仓库内已经包含一个本地 skill：

- `skills/leetcode-generate-problem`

这个 skill 对应的职责不是只生成题目，而是完整执行两段式流程：

1. 根据题号生成题目文件
2. 读取生成结果并补充更有价值的测试用例

#### skill 入口

- 说明文件：`skills/leetcode-generate-problem/SKILL.md`
- 包装脚本：`skills/leetcode-generate-problem/scripts/run_generate_problem.py`

#### skill 命令示例

```bash
python skills/leetcode-generate-problem/scripts/run_generate_problem.py 1
python skills/leetcode-generate-problem/scripts/run_generate_problem.py 1 --lang py
python skills/leetcode-generate-problem/scripts/run_generate_problem.py 1 --force
```

#### agent 使用方式

如果你是在支持本地 skill 的 agent 环境里使用这个仓库，可以直接显式调用：

```text
使用 $leetcode-generate-problem 生成第 1 题
使用 $leetcode-generate-problem 生成第 206 题，只要 Python
使用 $leetcode-generate-problem 重新生成第 1 题并覆盖已有文件
```

这个 skill 的默认要求是：

- 默认同时生成 `py` 和 `go`
- 默认不覆盖已有文件
- 生成后继续读取 `problems/*.json` 和代码文件
- 在预留的追加测试区域里补边界测试和特殊场景测试

## 文件结构

生成出来的代码文件内部固定分成几个区块：

- 题目信息
- `Solution` 代码
- 测试代码

Python 对于简单字面量题型会生成可直接运行的断言示例。Go 也会把简单题型的断言代码内嵌在同一个文件里。

像链表、二叉树这类需要构造复杂结构的题，当前版本会保留题面示例和占位说明，不会自动生成可执行断言。

## 生成后复查

推荐把这个仓库里的 skill 当成“两段式”工作流：

1. 先按题号生成单文件模板和题目元数据
2. 再让 agent 读取生成结果，补充更有价值的测试用例

当前生成器已经为这一步预留了稳定位置：

- Python 文件里有 `_run_additional_tests()`
- Go 文件里有 `selfTestAdditional()`
- `problems/*.json` 里保存了题面文本、约束、示例、签名和提示

这样 agent 可以基于题意和约束补边界测试，而不是只保留题目原始样例。

## 生成题解

使用 `make gen` 快捷生成题目模板：

```bash
make gen 121             # 同时生成 Go 和 Python
make gen 121 go          # 只生成 Go
make gen 121 py          # 只生成 Python
make gen 121 FORCE=1     # 覆盖已有文件
make gen 121 go FORCE=1  # 只生成 Go 并覆盖
```

## 运行题解

使用根目录的 `Makefile` 直接运行指定题号的题解文件：

```bash
make run 0121        # 两种语言都运行（可带前导零）
make run 121         # 等价，会自动补全为 0121
make run 0121 go     # 只运行 Go
make run 0121 py     # 只运行 Python
```

- 如果 Go 和 Python 文件都存在且未指定语言，两个都会依次运行。
- 如果只有其中一个存在，只运行那个。
- 如果两个都不存在，打印错误并以非零状态退出。

## 测试

运行生成器相关测试：

```bash
python -m unittest discover -s tests
```
