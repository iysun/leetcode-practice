from __future__ import annotations
from typing import List

# Problem: 0064 Minimum Path Sum
# URL: https://leetcode.cn/problems/minimum-path-sum/
# Difficulty: Medium
# Tags: Array, Dynamic Programming, Matrix
# Constraints:
# - m == grid.length
# - n == grid[i].length
# - 1 <= m, n <= 200
# - 0 <= grid[i][j] <= 200

# === Solution ===
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [grid[0][0]] * n
        for i in range(1, n):
            dp[i] = dp[i-1] + grid[0][i]
        for i in range(1, m):
            dp[0] += grid[i][0]
            for j in range(1, n):
                dp[j] = grid[i][j] + min(dp[j-1], dp[j])
        return dp[n-1]

# === Test Code ===
# Example 1
# Input: [[1,3,1],[1,5,1],[4,2,1]]
# Output: 7
# Example 2
# Input: [[1,2,3],[4,5,6]]
# Output: 12

def _run_examples() -> None:
    solver = Solution()
    assert solver.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7, "example 1 failed"
    assert solver.minPathSum([[1, 2, 3], [4, 5, 6]]) == 12, "example 2 failed"

def _run_additional_tests() -> None:
    # 最小网格 1x1
    assert Solution().minPathSum([[0]]) == 0
    # 单行，只能向右
    assert Solution().minPathSum([[1, 2, 3, 4]]) == 10
    # 单列，只能向下
    assert Solution().minPathSum([[1], [2], [3]]) == 6
    # 全零网格
    assert Solution().minPathSum([[0, 0], [0, 0]]) == 0
    # 2x2 全 1 网格，两条路径和均为 3
    assert Solution().minPathSum([[1, 1], [1, 1]]) == 3

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
