package main

// Problem: 0121 Best Time to Buy and Sell Stock
// URL: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
// Difficulty: Easy
// Tags: Array, Dynamic Programming
// Constraints:
// - 1 <= prices.length <= 10^5
// - 0 <= prices[i] <= 10^4

import "reflect"

// === Solution ===
func maxProfit(prices []int) int {
	panic("TODO: implement")
}

// === Test Code ===
// Example 1
// Input: [7,1,5,3,6,4]
// Output: 5
// Example 2
// Input: [7,6,4,3,1]
// Output: 0

func selfTest() {
	if got := maxProfit([]int{7, 1, 5, 3, 6, 4}); !reflect.DeepEqual(got, 5) {
		panic("example 1 failed")
	}
	if got := maxProfit([]int{7, 6, 4, 3, 1}); !reflect.DeepEqual(got, 0) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// Single element: no future day to sell
	if got := maxProfit([]int{5}); got != 0 {
		panic("single element failed")
	}
	// Two elements ascending
	if got := maxProfit([]int{1, 2}); got != 1 {
		panic("two elements ascending failed")
	}
	// All same prices: no profit
	if got := maxProfit([]int{3, 3, 3, 3}); got != 0 {
		panic("flat prices failed")
	}
	// Max constraint values: max possible profit (prices[i] in [0, 10^4])
	if got := maxProfit([]int{0, 10000}); got != 10000 {
		panic("max profit failed")
	}
	// General case: optimal is buy at 1 (index 1 or 3), sell at 9 (index 5)
	if got := maxProfit([]int{3, 1, 4, 1, 5, 9, 2, 6}); got != 8 {
		panic("mixed sequence failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
