# leetcode-practice — 项目约定

## LeetCode 题目生成

当用户提到 LeetCode 题号、"生成题目"、"同步题目"、"生成第 X 题"、"把第 X 题加进来"时，执行以下流程：

1. 从用户请求里提取数字题号。
2. 在项目根目录运行包装脚本：
   ```bash
   python skills/leetcode-generate-problem/scripts/run_generate_problem.py <题号>
   ```
   - 只有用户明确指定语言时才传 `--lang py` 或 `--lang go`，否则同时生成两种语言。
   - 除非用户明确要求覆盖，否则不传 `--force`。
3. 生成完成后，读取以下文件：
   - `problems/<id>_<slug>.json`
   - `solutions/py/<id>_<slug>.py`（如果生成了）
   - `solutions/go/<id>_<slug>.go`（如果生成了）
4. 根据题目描述、约束和示例，在以下预留位置补充 2–5 个高价值测试：
   - Python：`_run_additional_tests()` 函数体内
   - Go：`selfTestAdditional()` 函数体内
   - 优先补充：最小/最大边界输入、重复值、负数、零值、空串、输出顺序不固定的判定说明。
5. 把生成和补充后的文件路径返回给用户。

### 失败处理

- 缺少题号：要求用户提供数字形式的 LeetCode 前端题号。
- 文件已存在：告诉用户需要明确的覆盖请求才会传 `--force`。
- 语言不支持：只支持 `py` 和 `go`，其他语言直接说明并停止。
- 无法获取题面：直接返回错误，不要猜测题目内容。
