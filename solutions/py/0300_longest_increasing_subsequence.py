from __future__ import annotations
from typing import List

# Problem: 0300 Longest Increasing Subsequence
# URL: https://leetcode.cn/problems/longest-increasing-subsequence/
# Difficulty: Medium
# Tags: Array, Binary Search, Dynamic Programming
# Constraints:
# - 1 <= nums.length <= 2500
# - -10^4 <= nums[i] <= 10^4

# === Solution ===
class Solution:
    # dp 写法, dp[i] = max(dp[0...i] + 1)   O(n^2)
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1]*len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j]+1)
        return max(dp)


# === Test Code ===
# Example 1
# Input: [10,9,2,5,3,7,101,18]
# Output: 4
# Example 2
# Input: [0,1,0,3,2,3]
# Output: 4
# Example 3
# Input: [7,7,7,7,7,7,7]
# Output: 1

def _run_examples() -> None:
    solver = Solution()
    assert solver.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4, "example 1 failed"
    assert solver.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4, "example 2 failed"
    assert solver.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]) == 1, "example 3 failed"

def _run_additional_tests() -> None:
    # 单元素数组，最小输入
    assert Solution().lengthOfLIS([5]) == 1
    # 严格递减，无递增子序列
    assert Solution().lengthOfLIS([5, 4, 3, 2, 1]) == 1
    # 已严格递增
    assert Solution().lengthOfLIS([1, 2, 3, 4, 5]) == 5
    # 包含负数
    assert Solution().lengthOfLIS([-10, -2, 0, 3]) == 4
    # 有重复值的混合序列
    assert Solution().lengthOfLIS([-1, 0, -1, 2, 3]) == 4

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
