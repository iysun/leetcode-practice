package main

// Problem: 0062 Unique Paths
// URL: https://leetcode.cn/problems/unique-paths/
// Difficulty: Medium
// Tags: Math, Dynamic Programming, Combinatorics
// Constraints:
// - 1 <= m, n <= 100

import "reflect"

// === Solution ===
func uniquePaths(m int, n int) int {
	dp := make([]int, n)
	for i, _ := range dp {
		dp[i] = 1
	}
	for j := 1; j < m; j++ {
		for i := 1; i < n; i++ {
			dp[i] = dp[i] + dp[i-1]
		}
	}
	return dp[n-1]
}

// === Test Code ===
// Example 1
// Input: 3; 7
// Output: 28
// Example 2
// Input: 3; 2
// Output: 3

func selfTest() {
	if got := uniquePaths(3, 7); !reflect.DeepEqual(got, 28) {
		panic("example 1 failed")
	}
	if got := uniquePaths(3, 2); !reflect.DeepEqual(got, 3) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 最小网格 1x1
	if got := uniquePaths(1, 1); !reflect.DeepEqual(got, 1) {
		panic("1x1 grid failed")
	}
	// 单行：只有一种走法
	if got := uniquePaths(1, 100); !reflect.DeepEqual(got, 1) {
		panic("1x100 grid failed")
	}
	// 单列：只有一种走法
	if got := uniquePaths(100, 1); !reflect.DeepEqual(got, 1) {
		panic("100x1 grid failed")
	}
	// 2x2 网格
	if got := uniquePaths(2, 2); !reflect.DeepEqual(got, 2) {
		panic("2x2 grid failed")
	}
	// 3x3 网格
	if got := uniquePaths(3, 3); !reflect.DeepEqual(got, 6) {
		panic("3x3 grid failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
