package main

// Problem: 0001 Two Sum
// URL: https://leetcode.cn/problems/two-sum/
// Difficulty: Easy
// Tags: Array, Hash Table
// Constraints:
// - 2 <= nums.length <= 10^4
// - -10^9 <= nums[i] <= 10^9
// - -10^9 <= target <= 10^9
// - Only one valid answer exists.

import "reflect"

// === Solution ===
func twoSum(nums []int, target int) []int {
	panic("TODO: implement")
}

// === Test Code ===
// Example 1
// Input: [2,7,11,15]; 9
// Output: [0,1]
// Example 2
// Input: [3,2,4]; 6
// Output: [1,2]
// Example 3
// Input: [3,3]; 6
// Output: [0,1]

func selfTest() {
	if got := twoSum([]int{2, 7, 11, 15}, 9); !reflect.DeepEqual(got, []int{0, 1}) {
		panic("example 1 failed")
	}
	if got := twoSum([]int{3, 2, 4}, 6); !reflect.DeepEqual(got, []int{1, 2}) {
		panic("example 2 failed")
	}
	if got := twoSum([]int{3, 3}, 6); !reflect.DeepEqual(got, []int{0, 1}) {
		panic("example 3 failed")
	}
}
