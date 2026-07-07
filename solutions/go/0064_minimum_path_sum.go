package main

// Problem: 0064 Minimum Path Sum
// URL: https://leetcode.cn/problems/minimum-path-sum/
// Difficulty: Medium
// Tags: Array, Dynamic Programming, Matrix
// Constraints:
// - m == grid.length
// - n == grid[i].length
// - 1 <= m, n <= 200
// - 0 <= grid[i][j] <= 200

import "reflect"

// === Solution ===
func minPathSum(grid [][]int) int {
	m, n := len(grid), len(grid[0])
	dp := make([]int, n)
	dp[0] = grid[0][0]
	for i := 1; i < n; i++ {
		dp[i] = dp[i-1] + grid[0][i]
	}
	for i := 1; i < m; i++ {
		dp[0] += grid[i][0]
		for j := 1; j < n; j++ {
			dp[j] = grid[i][j] + min(dp[j-1], dp[j])
		}
	}
	return dp[n-1]
}

// === Test Code ===
// Example 1
// Input: [[1,3,1],[1,5,1],[4,2,1]]
// Output: 7
// Example 2
// Input: [[1,2,3],[4,5,6]]
// Output: 12

func selfTest() {
	if got := minPathSum([][]int{[]int{1, 3, 1}, []int{1, 5, 1}, []int{4, 2, 1}}); !reflect.DeepEqual(got, 7) {
		panic("example 1 failed")
	}
	if got := minPathSum([][]int{[]int{1, 2, 3}, []int{4, 5, 6}}); !reflect.DeepEqual(got, 12) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 最小网格 1x1
	if got := minPathSum([][]int{[]int{0}}); !reflect.DeepEqual(got, 0) {
		panic("1x1 grid failed")
	}
	// 单行，只能向右
	if got := minPathSum([][]int{[]int{1, 2, 3, 4}}); !reflect.DeepEqual(got, 10) {
		panic("1x4 grid failed")
	}
	// 单列，只能向下
	if got := minPathSum([][]int{[]int{1}, []int{2}, []int{3}}); !reflect.DeepEqual(got, 6) {
		panic("3x1 grid failed")
	}
	// 全零网格
	if got := minPathSum([][]int{[]int{0, 0}, []int{0, 0}}); !reflect.DeepEqual(got, 0) {
		panic("all zeros failed")
	}
	// 2x2 全 1 网格
	if got := minPathSum([][]int{[]int{1, 1}, []int{1, 1}}); !reflect.DeepEqual(got, 3) {
		panic("2x2 all ones failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
