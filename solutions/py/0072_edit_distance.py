from __future__ import annotations

# Problem: 0072 Edit Distance
# URL: https://leetcode.cn/problems/edit-distance/
# Difficulty: Medium
# Tags: String, Dynamic Programming
# Constraints:
# - 0 <= word1.length, word2.length <= 500
# - word1 and word2 consist of lowercase English letters.


# === Solution ===
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        if m * n == 0:
            return n + m
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(0, m + 1):
            dp[i][0] = i
        for i in range(0, n + 1):
            dp[0][i] = i
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                pre = dp[i - 1][j - 1]
                if word1[i - 1] != word2[j - 1]:
                    pre += 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, pre)
        return dp[m][n]


# === Test Code ===
# Example 1
# Input: "horse"; "ros"
# Output: 3
# Example 2
# Input: "intention"; "execution"
# Output: 5


def _run_examples() -> None:
    solver = Solution()
    assert solver.minDistance("horse", "ros") == 3, "example 1 failed"
    assert solver.minDistance("intention", "execution") == 5, "example 2 failed"


def _run_additional_tests() -> None:
    solver = Solution()
    # 两串都为空 -> 0（约束允许长度为 0）
    assert solver.minDistance("", "") == 0
    # 一串为空：全部靠插入，距离 = 另一串长度
    assert solver.minDistance("", "abc") == 3
    # 另一串为空：全部靠删除，距离 = 该串长度
    assert solver.minDistance("abc", "") == 3
    # 完全相同 -> 0，不应误判为需要操作
    assert solver.minDistance("abc", "abc") == 0
    # 等长且仅一处不同：一次替换即可，别当成删+插两步
    assert solver.minDistance("abc", "abd") == 1


if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
