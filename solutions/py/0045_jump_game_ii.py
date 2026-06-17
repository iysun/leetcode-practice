from __future__ import annotations
from typing import List

# Problem: 0045 Jump Game II
# URL: https://leetcode.cn/problems/jump-game-ii/
# Difficulty: Medium
# Tags: Greedy, Array, Dynamic Programming
# Constraints:
# - 1 <= nums.length <= 10^4
# - 0 <= nums[i] <= 1000
# - It's guaranteed that you can reach nums[n - 1].

# === Solution ===
class Solution:
    def jump(self, nums: List[int]) -> int:
        raise NotImplementedError

# === Test Code ===
# Example 1
# Input: [2,3,1,1,4]
# Output: 2
# Example 2
# Input: [2,3,0,1,4]
# Output: 2

def _run_examples() -> None:
    solver = Solution()
    assert solver.jump([2, 3, 1, 1, 4]) == 2, "example 1 failed"
    assert solver.jump([2, 3, 0, 1, 4]) == 2, "example 2 failed"

def _run_additional_tests() -> None:
    solver = Solution()
    # Single element: already at end
    assert solver.jump([0]) == 0, "single element failed"
    # Single jump covers everything
    assert solver.jump([5, 1, 1, 1, 1]) == 1, "first element reaches end failed"
    # All ones: must jump one step at a time
    assert solver.jump([1, 1, 1, 1, 1]) == 4, "all ones failed"
    # Two elements
    assert solver.jump([1, 0]) == 1, "two elements failed"
    # Large jumps available but not needed
    assert solver.jump([10, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 1, "large jump failed"
    # Zeros in middle, but reachable
    assert solver.jump([2, 0, 3, 0, 1]) == 2, "zeros in middle failed"
    # Optimal path requires choosing longer jump
    assert solver.jump([3, 2, 1, 0, 4]) == 2, "optimal path failed"

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
