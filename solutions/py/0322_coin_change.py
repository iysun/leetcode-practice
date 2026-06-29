from __future__ import annotations
from typing import List

# Problem: 0322 Coin Change
# URL: https://leetcode.cn/problems/coin-change/
# Difficulty: Medium
# Tags: Breadth-First Search, Array, Dynamic Programming
# Constraints:
# - 1 <= coins.length <= 12
# - 1 <= coins[i] <= 2^31 - 1
# - 0 <= amount <= 10^4

# === Solution ===
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount+1)
        dp[0] = 0
        for i in range(0, len(coins)):
            for j in range(coins[i], amount+1):
                dp[j] = min(dp[j-coins[i]]+1, dp[j])
        if dp[amount] == float('inf'):
            return -1
        return dp[amount]

# === Test Code ===
# Example 1
# Input: [1,2,5]; 11
# Output: 3
# Example 2
# Input: [2]; 3
# Output: -1
# Example 3
# Input: [1]; 0
# Output: 0

def _run_examples() -> None:
    solver = Solution()
    assert solver.coinChange([1, 2, 5], 11) == 3, "example 1 failed"
    assert solver.coinChange([2], 3) == -1, "example 2 failed"
    assert solver.coinChange([1], 0) == 0, "example 3 failed"

def _run_additional_tests() -> None:
    solver = Solution()
    # Zero amount always returns 0
    assert solver.coinChange([1, 2, 5], 0) == 0, "amount=0"
    # Only unit coin, large amount
    assert solver.coinChange([1], 10000) == 10000, "large amount with coin=1"
    # Cannot make amount
    assert solver.coinChange([5], 7) == -1, "unreachable amount"
    # Greedy trap: [1,3,4] amount=6, greedy picks 4+1+1=3, optimal is 3+3=2
    assert solver.coinChange([1, 3, 4], 6) == 2, "non-greedy case"
    # Multiple denominations
    assert solver.coinChange([1, 2, 5, 10], 27) == 4, "multiple coins"

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
