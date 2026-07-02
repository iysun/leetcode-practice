from __future__ import annotations

# Problem: 0032 Longest Valid Parentheses
# URL: https://leetcode.cn/problems/longest-valid-parentheses/
# Difficulty: Hard
# Tags: Stack, String, Dynamic Programming
# Constraints:
# - 0 <= s.length <= 3 * 10^4
# - s[i] is '(', or ')'.

# 有三种解法:
# 1. 栈记录无效右括号 2. dp 3. 双向基数(如果, 首字符为左括号, 尾字符尾右括号, 且左右括号数相同则为有效)
# 时间复杂度都是 O(n), 1、2 空间复杂度为 O(n), 3 空间复杂度为 O(1)


# === Solution ===
class Solution:
    # 栈解法, 使用一个哨兵-1, 用来处理右括号不匹配的情况
    # 遇到右括号无脑 pop, 如果有匹配的左括号 stack始终不为空
    # 否则会 pop -1, 或者其他右括号 下标 导致栈为空
    def longestValidParentheses1(self, s: str) -> int:
        if not s:
            return 0
        stack = [-1]  # 使用哨位
        ans = 0
        for i, c in enumerate(s):
            if c == "(":
                stack.append(i)
            else:
                stack.pop()
                if len(stack) == 0:
                    stack.append(i)
                    continue
                ans = max(ans, i - stack[-1])
        return ans

    # dp 动态规划
    # if c == '(' : dp[i] = 0    --- ()(()
    # if c == ')' :
    # if s[i-1] == '(' : dp[i] = dp[i-2] + 2
    # else s[i-1] == ')' : dp[i] = dp[i-1] + dp[i-dp[i-1]-2] + 2     ---  ()() (()()]
    def at(self, dp: list[int], i: int) -> int:
        if i < 0:
            return 0
        return dp[i]

    def longestValidParentheses(self, s: str) -> int:
        if not s:
            return 0
        dp = [0] * len(s)  # 只有一个括号时一定为0
        for i in range(1, len(s)):
            if s[i] == "(":
                continue

            if s[i - 1] == "(":
                dp[i] = self.at(dp, i - 2) + 2
                continue

            pre = i - dp[i - 1] - 1
            if pre >= 0 and s[pre] == "(":  # ()) => 2-2-1 = -1
                dp[i] = dp[i - 1] + self.at(dp, pre - 1) + 2
        return max(dp)

    # 最容易理解也是空间复杂度最低的方法, 双向遍历 遇到无效括号将 r l 重置为 0 同时处理左括号或右括号比较多的情况 (() | ())
    def longestValidParentheses2(self, s: str) -> int:
        if not s:
            return 0
        l, r = 0, 0
        ans = 0
        for i in range(len(s)):
            if s[i] == "(":
                l += 1
            else:
                r += 1
            if l == r:
                ans = max(ans, l + r)
            elif r > l:
                l, r = 0, 0
        l, r = 0, 0
        for i in range(len(s) - 1, -1, -1):
            if s[i] == ")":
                r += 1
            else:
                l += 1
            if l == r:
                ans = max(ans, l + r)
            elif l > r:
                l, r = 0, 0
        return ans


# === Test Code ===
# Example 1
# Input: "(()"
# Output: 2
# Example 2
# Input: ")()())"
# Output: 4
# Example 3
# Input: ""
# Output: 0


def _run_examples() -> None:
    solver = Solution()
    assert solver.longestValidParentheses("(()") == 2, "example 1 failed"
    assert solver.longestValidParentheses(")()())") == 4, "example 2 failed"
    assert solver.longestValidParentheses("") == 0, "example 3 failed"


def _run_additional_tests() -> None:
    # 最小非空输入且无法配对
    assert Solution().longestValidParentheses("(") == 0
    # 全是左括号时不存在任何有效连续子串
    assert Solution().longestValidParentheses("(((") == 0
    # 整个字符串都是有效括号并包含嵌套
    assert Solution().longestValidParentheses("()(())") == 6
    # 遇到无效断点后，应只统计后面连续有效的最长子串
    assert Solution().longestValidParentheses("())(())") == 4

    assert Solution().longestValidParentheses("()(()") == 2


if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
