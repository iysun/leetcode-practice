from __future__ import annotations

# Problem: 0062 Unique Paths
# URL: https://leetcode.cn/problems/unique-paths/
# Difficulty: Medium
# Tags: Math, Dynamic Programming, Combinatorics
# Constraints:
# - 1 <= m, n <= 100


# === Solution ===
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] = dp[j] + dp[j - 1]
        return dp[n - 1]


# === Test Code ===
# Example 1
# Input: 3; 7
# Output: 28
# Example 2
# Input: 3; 2
# Output: 3


def _run_examples() -> None:
    solver = Solution()
    assert solver.uniquePaths(3, 7) == 28, "example 1 failed"
    assert solver.uniquePaths(3, 2) == 3, "example 2 failed"


def _run_additional_tests() -> None:
    # 最小网格 1x1
    assert Solution().uniquePaths(1, 1) == 1
    # 单行：只有一种走法
    assert Solution().uniquePaths(1, 100) == 1
    # 单列：只有一种走法
    assert Solution().uniquePaths(100, 1) == 1
    # 2x2 网格
    assert Solution().uniquePaths(2, 2) == 2
    # 3x3 网格
    assert Solution().uniquePaths(3, 3) == 6


if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
