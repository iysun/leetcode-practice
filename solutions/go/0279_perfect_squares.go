package main

// Problem: 0279 Perfect Squares
// URL: https://leetcode.cn/problems/perfect-squares/
// Difficulty: Medium
// Tags: Breadth-First Search, Math, Dynamic Programming
// Constraints:
// - 1 <= n <= 10^4

import (
	"math"
	"reflect"
)

// === Solution ===
func numSquares(n int) int {
	dp := make([]int, n+1)
	for i, _ := range dp {
		dp[i] = math.MaxInt32
	}
	dp[0] = 0
	for i, _ := range dp {
		for j := 1; j*j <= i; j++ {
			dp[i] = min(dp[i], dp[i-j*j]+1)
		}
	}
	return dp[n]
}

// === Test Code ===
// Example 1
// Input: 12
// Output: 3
// Example 2
// Input: 13
// Output: 2

func selfTest() {
	if got := numSquares(12); !reflect.DeepEqual(got, 3) {
		panic("example 1 failed")
	}
	if got := numSquares(13); !reflect.DeepEqual(got, 2) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// Min input
	if got := numSquares(1); !reflect.DeepEqual(got, 1) {
		panic("n=1 should be 1 (1 itself)")
	}
	// n is a perfect square
	if got := numSquares(4); !reflect.DeepEqual(got, 1) {
		panic("n=4 is 2^2")
	}
	// Lagrange's four-square theorem: at most 4 squares
	if got := numSquares(7); !reflect.DeepEqual(got, 4) {
		panic("n=7 = 4+1+1+1")
	}
	if got := numSquares(2); !reflect.DeepEqual(got, 2) {
		panic("n=2 = 1+1")
	}
	// Max constraint boundary
	if got := numSquares(10000); !reflect.DeepEqual(got, 1) {
		panic("n=10000 is 100^2")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
