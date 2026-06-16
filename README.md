# leetcode-practice

用于把 LeetCode 题目同步到本地，并生成单文件模板。每道题每种语言只生成一个文件，文件里同时包含示例代码和测试代码，用注释分区隔开。

## 说明

目前支持两种语言：

- `py/`: Python 单文件模板
- `go/`: Go 单文件模板

同时会在 `problems/` 下保存一份精简题面元数据，包含标题、链接、签名、示例和约束。

## 使用

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

- `py/0001_two_sum.py`
- `go/0001_two_sum.go`
- `problems/0001_two_sum.json`

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

## 测试

运行生成器相关测试：

```bash
python -m unittest discover -s tests
```
