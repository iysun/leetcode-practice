from __future__ import annotations
from typing import List

# Problem: 0416 Partition Equal Subset Sum
# URL: https://leetcode.cn/problems/partition-equal-subset-sum/
# Difficulty: Medium
# Tags: Array, Dynamic Programming
# Constraints:
# - 1 <= nums.length <= 200
# - 1 <= nums[i] <= 100

# === Solution ===
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        S = sum(nums)
        if S % 2 == 1:
            return False
        W = int(S/2)
        dp = [False] * (W+1)
        dp[0] = True
        for num in nums:
            for j in range(W, num-1, -1):
                if dp[j-num]: dp[j] = True
        return dp[W]
                

# === Test Code ===
# Example 1
# Input: [1,5,11,5]
# Output: true
# Example 2
# Input: [1,2,3,5]
# Output: false

def _run_examples() -> None:
    solver = Solution()
    assert solver.canPartition([1, 5, 11, 5]) == True, "example 1 failed"
    assert solver.canPartition([1, 2, 3, 5]) == False, "example 2 failed"

def _run_additional_tests() -> None:
    # 单元素数组，总和为奇数不可分割
    assert Solution().canPartition([1]) is False
    # 两个相等元素可各分一个
    assert Solution().canPartition([1, 1]) is True
    # 总和为偶数且可分割 [1,2] 与 [3]
    assert Solution().canPartition([1, 2, 3]) is True
    # 四个相同元素可平分成两组
    assert Solution().canPartition([2, 2, 2, 2]) is True
    # 总和为偶数但无法凑出 target
    assert Solution().canPartition([1, 2, 5]) is False

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
