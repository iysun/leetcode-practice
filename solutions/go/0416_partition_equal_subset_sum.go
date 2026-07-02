package main

// Problem: 0416 Partition Equal Subset Sum
// URL: https://leetcode.cn/problems/partition-equal-subset-sum/
// Difficulty: Medium
// Tags: Array, Dynamic Programming
// Constraints:
// - 1 <= nums.length <= 200
// - 1 <= nums[i] <= 100

import "reflect"

// === Solution ===
func canPartition(nums []int) bool {
	sum := 0
	for _, v := range nums {
		sum += v
	}
	if sum%2 == 1 {
		return false
	}
	sum /= 2
	dp := make([]bool, sum+1)
	dp[0] = true
	for _, v := range nums {
		for j := sum; j >= v; j-- {
			if dp[j-v] == true {
				dp[j] = true
			}
		}
	}
	return dp[sum]
}

// === Test Code ===
// Example 1
// Input: [1,5,11,5]
// Output: true
// Example 2
// Input: [1,2,3,5]
// Output: false

func selfTest() {
	if got := canPartition([]int{1, 5, 11, 5}); !reflect.DeepEqual(got, true) {
		panic("example 1 failed")
	}
	if got := canPartition([]int{1, 2, 3, 5}); !reflect.DeepEqual(got, false) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 单元素数组，总和为奇数不可分割
	if got := canPartition([]int{1}); !reflect.DeepEqual(got, false) {
		panic("single element failed")
	}
	// 两个相等元素可各分一个
	if got := canPartition([]int{1, 1}); !reflect.DeepEqual(got, true) {
		panic("two equal elements failed")
	}
	// 总和为偶数且可分割 [1,2] 与 [3]
	if got := canPartition([]int{1, 2, 3}); !reflect.DeepEqual(got, true) {
		panic("even sum partitionable failed")
	}
	// 四个相同元素可平分成两组
	if got := canPartition([]int{2, 2, 2, 2}); !reflect.DeepEqual(got, true) {
		panic("four equal elements failed")
	}
	// 总和为偶数但无法凑出 target
	if got := canPartition([]int{1, 2, 5}); !reflect.DeepEqual(got, false) {
		panic("even sum impossible failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
