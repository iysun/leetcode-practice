package main

// Problem: 0300 Longest Increasing Subsequence
// URL: https://leetcode.cn/problems/longest-increasing-subsequence/
// Difficulty: Medium
// Tags: Array, Binary Search, Dynamic Programming
// Constraints:
// - 1 <= nums.length <= 2500
// - -10^4 <= nums[i] <= 10^4

import (
	"reflect"
)

// === Solution ===
func lengthOfLIS(nums []int) int {
	// 贪心+二分查找 O(n*log(n))
	tails := make([]int, 0, len(nums))
	for _, x := range nums {
		i, right := 0, len(tails)
		for i < right {
			mid := i + (right-i)/2
			if tails[mid] < x {
				i = mid + 1
			} else {
				right = mid
			}
		}
		if i == len(tails) {
			tails = append(tails, x)
		} else {
			tails[i] = x
		}
	}
	return len(tails)
}

// === Test Code ===
// Example 1
// Input: [10,9,2,5,3,7,101,18]
// Output: 4
// Example 2
// Input: [0,1,0,3,2,3]
// Output: 4
// Example 3
// Input: [7,7,7,7,7,7,7]
// Output: 1

func selfTest() {
	if got := lengthOfLIS([]int{10, 9, 2, 5, 3, 7, 101, 18}); !reflect.DeepEqual(got, 4) {
		panic("example 1 failed")
	}
	if got := lengthOfLIS([]int{0, 1, 0, 3, 2, 3}); !reflect.DeepEqual(got, 4) {
		panic("example 2 failed")
	}
	if got := lengthOfLIS([]int{7, 7, 7, 7, 7, 7, 7}); !reflect.DeepEqual(got, 1) {
		panic("example 3 failed")
	}
}

func selfTestAdditional() {
	// 单元素数组，最小输入
	if got := lengthOfLIS([]int{5}); !reflect.DeepEqual(got, 1) {
		panic("single element failed")
	}
	// 严格递减，无递增子序列
	if got := lengthOfLIS([]int{5, 4, 3, 2, 1}); !reflect.DeepEqual(got, 1) {
		panic("strictly decreasing failed")
	}
	// 已严格递增
	if got := lengthOfLIS([]int{1, 2, 3, 4, 5}); !reflect.DeepEqual(got, 5) {
		panic("strictly increasing failed")
	}
	// 包含负数
	if got := lengthOfLIS([]int{-10, -2, 0, 3}); !reflect.DeepEqual(got, 4) {
		panic("with negatives failed")
	}
	// 有重复值的混合序列
	if got := lengthOfLIS([]int{-1, 0, -1, 2, 3}); !reflect.DeepEqual(got, 4) {
		panic("mixed with duplicates failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
