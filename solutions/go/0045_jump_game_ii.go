package main

// Problem: 0045 Jump Game II
// URL: https://leetcode.cn/problems/jump-game-ii/
// Difficulty: Medium
// Tags: Greedy, Array, Dynamic Programming
// Constraints:
// - 1 <= nums.length <= 10^4
// - 0 <= nums[i] <= 1000
// - It's guaranteed that you can reach nums[n - 1].

import "reflect"

// === Solution ===
func jump(nums []int) int {
	current_end, farthest, jumps := 0, 0, 0

	for i := range nums[:len(nums)-1] {
		farthest = max(farthest, i+nums[i])
		if i == current_end {
			jumps += 1
			current_end = farthest
		}
	}
	return jumps
}

// === Test Code ===
// Example 1
// Input: [2,3,1,1,4]
// Output: 2
// Example 2
// Input: [2,3,0,1,4]
// Output: 2

func selfTest() {
	if got := jump([]int{2, 3, 1, 1, 4}); !reflect.DeepEqual(got, 2) {
		panic("example 1 failed")
	}
	if got := jump([]int{2, 3, 0, 1, 4}); !reflect.DeepEqual(got, 2) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// Single element: already at end
	if got := jump([]int{0}); !reflect.DeepEqual(got, 0) {
		panic("single element failed")
	}
	// Single jump covers everything
	if got := jump([]int{5, 1, 1, 1, 1}); !reflect.DeepEqual(got, 1) {
		panic("first element reaches end failed")
	}
	// All ones: must jump one step at a time
	if got := jump([]int{1, 1, 1, 1, 1}); !reflect.DeepEqual(got, 4) {
		panic("all ones failed")
	}
	// Two elements
	if got := jump([]int{1, 0}); !reflect.DeepEqual(got, 1) {
		panic("two elements failed")
	}
	// Large jumps available but not needed
	if got := jump([]int{10, 1, 1, 1, 1, 1, 1, 1, 1, 1}); !reflect.DeepEqual(got, 1) {
		panic("large jump failed")
	}
	// Zeros in middle, but reachable
	if got := jump([]int{2, 0, 3, 0, 1}); !reflect.DeepEqual(got, 2) {
		panic("zeros in middle failed")
	}
	// Optimal path requires choosing longer jump
	if got := jump([]int{3, 2, 1, 0, 4}); !reflect.DeepEqual(got, 2) {
		panic("optimal path failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
