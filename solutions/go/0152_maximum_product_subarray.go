package main

// Problem: 0152 Maximum Product Subarray
// URL: https://leetcode.cn/problems/maximum-product-subarray/
// Difficulty: Medium
// Tags: Array, Dynamic Programming
// Constraints:
// - 1 <= nums.length <= 2 * 10^4
// - -10 <= nums[i] <= 10
// - The product of any subarray of nums is guaranteed to fit in a 32-bit integer.

import "reflect"

// === Solution ===
func maxProduct(nums []int) int {
	n := len(nums)
	n_min, n_max, ans := nums[0], nums[0], nums[0]
	for i := 1; i < n; i++ {
		m, n := n_max*nums[i], n_min*nums[i]
		n_max = max(m, n, nums[i])
		n_min = min(m, n, nums[i])
		ans = max(n_max, ans)
	}
	return ans
}

// === Test Code ===
// Example 1
// Input: [2,3,-2,4]
// Output: 6
// Example 2
// Input: [-2,0,-1]
// Output: 0

func selfTest() {
	if got := maxProduct([]int{2, 3, -2, 4}); !reflect.DeepEqual(got, 6) {
		panic("example 1 failed")
	}
	if got := maxProduct([]int{-2, 0, -1}); !reflect.DeepEqual(got, 0) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 单元素数组（最小长度边界）
	if got := maxProduct([]int{5}); !reflect.DeepEqual(got, 5) {
		panic("single element failed")
	}
	// 全部负数且个数为奇数，需跳过其中一个负数
	if got := maxProduct([]int{-1, -2, -3, -4}); !reflect.DeepEqual(got, 24) {
		panic("all negatives odd count failed")
	}
	// 零值分割数组，乘积归零后重新累积
	if got := maxProduct([]int{-2, 0, 3}); !reflect.DeepEqual(got, 3) {
		panic("zero split failed")
	}
	// 正负交替，需同时维护最大/最小乘积
	if got := maxProduct([]int{2, -5, -2, -4, 3}); !reflect.DeepEqual(got, 24) {
		panic("alternating signs failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
