package main

// Problem: 0055 Jump Game
// URL: https://leetcode.cn/problems/jump-game/
// Difficulty: Medium
// Tags: Greedy, Array, Dynamic Programming
// Constraints:
// - 1 <= nums.length <= 10^4
// - 0 <= nums[i] <= 10^5

import "reflect"

// === Solution ===
func canJump(nums []int) bool {
	max_reach := 0

	for i, v := range nums {
		if i > max_reach {
			return false
		}
		max_reach = max(max_reach, i+v)
	}
	return true
}

// === Test Code ===
// Example 1
// Input: [2,3,1,1,4]
// Output: true
// Example 2
// Input: [3,2,1,0,4]
// Output: false

func selfTest() {
	if got := canJump([]int{2, 3, 1, 1, 4}); !reflect.DeepEqual(got, true) {
		panic("example 1 failed")
	}
	if got := canJump([]int{3, 2, 1, 0, 4}); !reflect.DeepEqual(got, false) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 1. Single element (minimum constraint)
	if got := canJump([]int{0}); !reflect.DeepEqual(got, true) {
		panic("single element failed")
	}
	// 2. First element is 0, can't move
	if got := canJump([]int{0, 2, 3}); !reflect.DeepEqual(got, false) {
		panic("blocked at start failed")
	}
	// 3. Jump over zeros to end
	if got := canJump([]int{2, 0, 0}); !reflect.DeepEqual(got, true) {
		panic("jump over zeros failed")
	}
	// 4. Large jump from first position covers entire array
	if got := canJump([]int{10, 0, 0, 0, 0}); !reflect.DeepEqual(got, true) {
		panic("large initial jump failed")
	}
	// 5. Need intermediate jumps to bypass zero
	if got := canJump([]int{1, 2, 0, 1}); !reflect.DeepEqual(got, true) {
		panic("intermediate jumps failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
