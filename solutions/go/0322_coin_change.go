package main

// Problem: 0322 Coin Change
// URL: https://leetcode.cn/problems/coin-change/
// Difficulty: Medium
// Tags: Breadth-First Search, Array, Dynamic Programming
// Constraints:
// - 1 <= coins.length <= 12
// - 1 <= coins[i] <= 2^31 - 1
// - 0 <= amount <= 10^4

import (
	"math"
	"reflect"
)

// === Solution ===
func coinChange(coins []int, amount int) int {
	dp := make([]int, amount+1)
	for i, _ := range dp {
		dp[i] = math.MaxInt32
	}
	dp[0] = 0
	for i, _ := range coins {
		for j := coins[i]; j <= amount; j++ {
			dp[j] = min(dp[j-coins[i]]+1, dp[j])
		}
	}
	if dp[amount] == math.MaxInt32 {
		return -1
	}
	return dp[amount]
}

// === Test Code ===
// Example 1
// Input: [1,2,5]; 11
// Output: 3
// Example 2
// Input: [2]; 3
// Output: -1
// Example 3
// Input: [1]; 0
// Output: 0

func selfTest() {
	if got := coinChange([]int{1, 2, 5}, 11); !reflect.DeepEqual(got, 3) {
		panic("example 1 failed")
	}
	if got := coinChange([]int{2}, 3); !reflect.DeepEqual(got, -1) {
		panic("example 2 failed")
	}
	if got := coinChange([]int{1}, 0); !reflect.DeepEqual(got, 0) {
		panic("example 3 failed")
	}
}

func selfTestAdditional() {
	// Zero amount always returns 0
	if got := coinChange([]int{1, 2, 5}, 0); !reflect.DeepEqual(got, 0) {
		panic("amount=0")
	}
	// Only unit coin, large amount
	if got := coinChange([]int{1}, 10000); !reflect.DeepEqual(got, 10000) {
		panic("large amount with coin=1")
	}
	// Cannot make amount
	if got := coinChange([]int{5}, 7); !reflect.DeepEqual(got, -1) {
		panic("unreachable amount")
	}
	// Greedy trap: [1,3,4] amount=6, greedy picks 4+1+1=3, optimal is 3+3=2
	if got := coinChange([]int{1, 3, 4}, 6); !reflect.DeepEqual(got, 2) {
		panic("non-greedy case")
	}
	// Multiple denominations
	if got := coinChange([]int{1, 2, 5, 10}, 27); !reflect.DeepEqual(got, 4) {
		panic("multiple coins")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
