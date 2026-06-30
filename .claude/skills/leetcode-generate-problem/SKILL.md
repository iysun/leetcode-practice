---
name: leetcode-generate-problem
description: 根据 LeetCode 前端题号调用当前仓库的生成器，生成本地题目文件。用于用户想把某道 LeetCode 题同步到这个仓库、生成 Python 或 Go 的单文件模板、补齐题目元数据，或重新生成已经存在的题目文件时。
---

# LeetCode 题目生成

根据前端题号生成当前仓库里的 LeetCode 题目文件，并在生成后复查结果，补充更有价值的测试用例。这个 skill 负责“输入题号，产出本地代码和元数据文件，然后继续阅读并优化测试”这条工作流。

## 默认流程

1. 确认用户是在当前仓库里生成 LeetCode 题目。
2. 从用户请求里提取前端题号。
3. 在仓库根目录运行 `.claude/skills/leetcode-generate-problem/scripts/run_generate_problem.py`。
4. 只有用户明确限制语言时才传 `--lang py` 或 `--lang go`，否则默认同时生成两种语言。
5. 除非用户明确要求覆盖已有文件，否则不要传 `--force`。
6. 生成完成后，立即读取生成出的语言文件和 `problems/<id>_<slug>.json`。
7. **补充测试用例（必做）**：只编辑 `_run_additional_tests()`（Python）/ `selfTestAdditional()`（Go）函数体，新增 2–5 条高价值断言，覆盖边界、特殊输入、顺序无关判定，或复杂结构的测试占位说明。
8. 只动追加测试函数体，不要打乱已有样例区（`_run_examples`/`selfTest`），也不要改解法桩。断言里的期望值可由你依题意推导后写入，但**不要实现解法主体**——解法由用户自己写。
9. **不要运行测试**：解法是桩，跑测试必然失败，属预期；不要为了让它通过而实现解法。
10. 完成后把生成和补充后的文件路径返回给用户，并说明解法主体仍是待实现的桩。

## 命令

从仓库根目录运行包装脚本：

```bash
python .claude/skills/leetcode-generate-problem/scripts/run_generate_problem.py 1
python .claude/skills/leetcode-generate-problem/scripts/run_generate_problem.py 1 --lang py
python .claude/skills/leetcode-generate-problem/scripts/run_generate_problem.py 1 --force
```

这个包装脚本会转调仓库根目录下的 `scripts/generate_problem.py`。

生成后继续读取：

- `problems/<id>_<slug>.json`
- `solutions/py/<id>_<slug>.py`
- `solutions/go/<id>_<slug>.go`

## 失败处理

- 如果缺少题号，要求用户提供数字形式的 LeetCode 前端题号。
- 如果因为文件已存在而生成失败，明确告诉用户需要 `--force` 或明确的覆盖请求。
- 如果无法获取 LeetCode 元数据，直接返回错误，不要猜测题面内容。
- 如果用户要求的语言不是 `py` 或 `go`，停止并说明当前只支持这两种语言。
- 如果题型需要链表、二叉树或其他复杂结构，而当前生成器没有自动构造器，先保留样例区，再在追加测试区写出待补的结构构造说明或手工测试骨架。

## 输出约定

成功时应生成：

- 请求 Python 时生成 `solutions/py/<id>_<slug>.py`
- 请求 Go 时生成 `solutions/go/<id>_<slug>.go`
- 始终生成 `problems/<id>_<slug>.json`

每个语言文件都是单文件结构，内部至少包含：

- 题目信息注释
- 解题代码骨架
- 用注释分隔的测试 / 示例代码区

Python 文件里会额外预留 `_run_additional_tests()`。
Go 文件里会额外预留 `selfTestAdditional()`。

复查后应优先在这些位置补充：

- 最小输入规模
- 最大或接近边界的输入规模
- 重复值、负数、零值、空串等特殊值
- 输出顺序不固定时的判定说明
- 容易被朴素实现漏掉的分支

## 资源

### scripts/

- `scripts/run_generate_problem.py`：对仓库生成器的薄包装。优先使用它，不要每次手写到根目录脚本的相对路径。

## 复查要求

生成完成后不要立刻结束。至少做这几步：

1. 读取元数据 JSON，确认题意、示例、约束和签名是否完整。
2. 读取生成出来的目标语言文件，确认样例测试是否和签名一致。
3. 判断题目是否适合直接增加可执行测试：
   - 基本类型、数组、字符串题：直接补充断言。
   - 链表、树、图等复杂结构题：补充构造器 TODO 或手工测试骨架。
4. 优先新增 2 到 5 个高价值测试，不要机械堆数量。
5. 新增测试必须与题目约束或常见错误路径有关，避免无意义重复样例。
6. 断言里的期望值可由你依题意/约束推导后写入，但**禁止实现题目解法主体**——保留 `Solution` 桩与样例区不动，只补追加测试函数体。
7. **不要运行测试**：解法是桩，跑测试必然失败，这是预期，不要为了通过而去实现解法。
