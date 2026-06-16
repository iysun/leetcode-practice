from __future__ import annotations
from typing import List

# Problem: 0001 Two Sum
# URL: https://leetcode.cn/problems/two-sum/
# Difficulty: Easy
# Tags: Array, Hash Table
# Constraints:
# - 2 <= nums.length <= 10^4
# - -10^9 <= nums[i] <= 10^9
# - -10^9 <= target <= 10^9
# - Only one valid answer exists.

# === Solution ===
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        raise NotImplementedError

# === Test Code ===
# Example 1
# Input: [2,7,11,15]; 9
# Output: [0,1]
# Example 2
# Input: [3,2,4]; 6
# Output: [1,2]
# Example 3
# Input: [3,3]; 6
# Output: [0,1]

def _run_examples() -> None:
    solver = Solution()
    assert solver.twoSum([2, 7, 11, 15], 9) == [0, 1], "example 1 failed"
    assert solver.twoSum([3, 2, 4], 6) == [1, 2], "example 2 failed"
    assert solver.twoSum([3, 3], 6) == [0, 1], "example 3 failed"

def _run_additional_tests() -> None:
    # Add boundary cases and special-case assertions after reviewing
    # the generated file together with problems/<id>_<slug>.json.
    pass

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
