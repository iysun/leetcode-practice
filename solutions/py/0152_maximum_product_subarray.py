from __future__ import annotations
from typing import List

# Problem: 0152 Maximum Product Subarray
# URL: https://leetcode.cn/problems/maximum-product-subarray/
# Difficulty: Medium
# Tags: Array, Dynamic Programming
# Constraints:
# - 1 <= nums.length <= 2 * 10^4
# - -10 <= nums[i] <= 10
# - The product of any subarray of nums is guaranteed to fit in a 32-bit integer.

# === Solution ===
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        ans = dp_max = dp_min = nums[0]
        for i in range(1, n):
            x = nums[i]
            m, n = dp_max*x, dp_min*x
            dp_max = max(m, n, x)
            dp_min = min(m, n, x)
            ans = max(dp_max, ans)
        
        return ans

# === Test Code ===
# Example 1
# Input: [2,3,-2,4]
# Output: 6
# Example 2
# Input: [-2,0,-1]
# Output: 0

def _run_examples() -> None:
    solver = Solution()
    assert solver.maxProduct([2, 3, -2, 4]) == 6, "example 1 failed"
    assert solver.maxProduct([-2, 0, -1]) == 0, "example 2 failed"

def _run_additional_tests() -> None:
    # 单元素数组（最小长度边界）
    assert Solution().maxProduct([5]) == 5
    # 全部负数且个数为奇数，需跳过其中一个负数
    assert Solution().maxProduct([-1, -2, -3, -4]) == 24
    # 零值分割数组，乘积归零后重新累积
    assert Solution().maxProduct([-2, 0, 3]) == 3
    # 正负交替，需同时维护最大/最小乘积
    assert Solution().maxProduct([2, -5, -2, -4, 3]) == 24

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
