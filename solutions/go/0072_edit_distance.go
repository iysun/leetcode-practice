package main

// Problem: 0072 Edit Distance
// URL: https://leetcode.cn/problems/edit-distance/
// Difficulty: Medium
// Tags: String, Dynamic Programming
// Constraints:
// - 0 <= word1.length, word2.length <= 500
// - word1 and word2 consist of lowercase English letters.

import "reflect"

// === Solution ===
func minDistance(word1 string, word2 string) int {
	m, n := len(word1), len(word2)
	dp := make([][]int, m+1)
	for i, _ := range dp {
		dp[i] = make([]int, n+1)
		dp[i][0] = i
	}
	for i := 0; i < n+1; i++ {
		dp[0][i] = i
	}

	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			pre := dp[i][j]
			if word1[i] != word2[j] {
				pre++
			}
			dp[i+1][j+1] = min(dp[i][j+1]+1, dp[i+1][j]+1, pre)
		}
	}
	return dp[m][n]
}

// === Test Code ===
// Example 1
// Input: "horse"; "ros"
// Output: 3
// Example 2
// Input: "intention"; "execution"
// Output: 5

func selfTest() {
	if got := minDistance("horse", "ros"); !reflect.DeepEqual(got, 3) {
		panic("example 1 failed")
	}
	if got := minDistance("intention", "execution"); !reflect.DeepEqual(got, 5) {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 两串都为空 -> 0（约束允许长度为 0）
	if got := minDistance("", ""); !reflect.DeepEqual(got, 0) {
		panic("both empty failed")
	}
	// 一串为空：全部靠插入，距离 = 另一串长度
	if got := minDistance("", "abc"); !reflect.DeepEqual(got, 3) {
		panic("empty word1 failed")
	}
	// 另一串为空：全部靠删除，距离 = 该串长度
	if got := minDistance("abc", ""); !reflect.DeepEqual(got, 3) {
		panic("empty word2 failed")
	}
	// 完全相同 -> 0，不应误判为需要操作
	if got := minDistance("abc", "abc"); !reflect.DeepEqual(got, 0) {
		panic("identical failed")
	}
	// 等长且仅一处不同：一次替换即可，别当成删+插两步
	if got := minDistance("abc", "abd"); !reflect.DeepEqual(got, 1) {
		panic("single replace failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
