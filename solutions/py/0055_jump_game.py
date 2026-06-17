from __future__ import annotations

from typing import List

# Problem: 0055 Jump Game
# URL: https://leetcode.cn/problems/jump-game/
# Difficulty: Medium
# Tags: Greedy, Array, Dynamic Programming
# Constraints:
# - 1 <= nums.length <= 10^4
# - 0 <= nums[i] <= 10^5


# === Solution ===
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0

        for i,v in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i+v)

        return True


# === Test Code ===
# Example 1
# Input: [2,3,1,1,4]
# Output: true
# Example 2
# Input: [3,2,1,0,4]
# Output: false


def _run_examples() -> None:
    solver = Solution()
    assert solver.canJump([2, 3, 1, 1, 4]) == True, "example 1 failed"
    assert solver.canJump([3, 2, 1, 0, 4]) == False, "example 2 failed"


def _run_additional_tests() -> None:
    solver = Solution()
    # 1. Single element (minimum constraint)
    assert solver.canJump([0]) == True, "single element failed"
    # 2. First element is 0, can't move
    assert solver.canJump([0, 2, 3]) == False, "blocked at start failed"
    # 3. Jump over zeros to end
    assert solver.canJump([2, 0, 0]) == True, "jump over zeros failed"
    # 4. Large jump from first position covers entire array
    assert solver.canJump([10, 0, 0, 0, 0]) == True, "large initial jump failed"
    # 5. Need intermediate jumps to bypass zero
    assert solver.canJump([1, 2, 0, 1]) == True, "intermediate jumps failed"


if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
