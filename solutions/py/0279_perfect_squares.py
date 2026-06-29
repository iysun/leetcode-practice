from __future__ import annotations

# Problem: 0279 Perfect Squares
# URL: https://leetcode.cn/problems/perfect-squares/
# Difficulty: Medium
# Tags: Breadth-First Search, Math, Dynamic Programming
# Constraints:
# - 1 <= n <= 10^4

# === Solution ===
class Solution:
    def numSquares(self, n: int) -> int:
        dp = [float('inf')] * (n+1)
        dp[0] = 0
        for i in range(1, n+1):
            j = 1
            while j*j <= i:
                dp[i] = min(dp[i], dp[i-j*j]+1)
                j+=1
        return dp[n]

# === Test Code ===
# Example 1
# Input: 12
# Output: 3
# Example 2
# Input: 13
# Output: 2

def _run_examples() -> None:
    solver = Solution()
    assert solver.numSquares(12) == 3, "example 1 failed"
    assert solver.numSquares(13) == 2, "example 2 failed"

def _run_additional_tests() -> None:
    solver = Solution()
    # Min input
    assert solver.numSquares(1) == 1, "n=1 should be 1 (1 itself)"
    # n is a perfect square
    assert solver.numSquares(4) == 1, "n=4 is 2^2"
    # Lagrange's four-square theorem: at most 4 squares
    assert solver.numSquares(7) == 4, "n=7 = 4+1+1+1"
    assert solver.numSquares(2) == 2, "n=2 = 1+1"
    # Max constraint boundary
    assert solver.numSquares(10000) == 1, "n=10000 is 100^2"

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
