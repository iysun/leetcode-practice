from __future__ import annotations
from typing import List

# Problem: 0121 Best Time to Buy and Sell Stock
# URL: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
# Difficulty: Easy
# Tags: Array, Dynamic Programming
# Constraints:
# - 1 <= prices.length <= 10^5
# - 0 <= prices[i] <= 10^4

# === Solution ===
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        raise NotImplementedError

# === Test Code ===
# Example 1
# Input: [7,1,5,3,6,4]
# Output: 5
# Example 2
# Input: [7,6,4,3,1]
# Output: 0

def _run_examples() -> None:
    solver = Solution()
    assert solver.maxProfit([7, 1, 5, 3, 6, 4]) == 5, "example 1 failed"
    assert solver.maxProfit([7, 6, 4, 3, 1]) == 0, "example 2 failed"

def _run_additional_tests() -> None:
    solver = Solution()
    # Single element: no future day to sell
    assert solver.maxProfit([5]) == 0, "single element failed"
    # Two elements ascending
    assert solver.maxProfit([1, 2]) == 1, "two elements ascending failed"
    # All same prices: no profit
    assert solver.maxProfit([3, 3, 3, 3]) == 0, "flat prices failed"
    # Max constraint values: max possible profit (prices[i] in [0, 10^4])
    assert solver.maxProfit([0, 10000]) == 10000, "max profit failed"
    # General case: optimal is buy at 1 (index 1 or 3), sell at 9 (index 5)
    assert solver.maxProfit([3, 1, 4, 1, 5, 9, 2, 6]) == 8, "mixed sequence failed"

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
