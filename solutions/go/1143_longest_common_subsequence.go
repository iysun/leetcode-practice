package main

// Problem: 1143 Longest Common Subsequence
// URL: https://leetcode.cn/problems/longest-common-subsequence/
// Difficulty: Medium
// Tags: String, Dynamic Programming
// Constraints:
// - 1 <= text1.length, text2.length <= 1000
// - text1 and text2 consist of only lowercase English characters.

import "reflect"

// === Solution ===
func longestCommonSubsequence(text1 string, text2 string) int {
	m, n := len(text1), len(text2)
	dp := make([][]int, m+1)
	for i, _ := range dp {
		dp[i] = make([]int, n+1)
	}

	for i, _ := range text1 {
		for j, _ := range text2 {
			if text1[i] == text2[j] {
				dp[i+1][j+1] = dp[i][j] + 1
			} else {
				dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
			}
		}
	}

	return dp[m][n]
}

// === Test Code ===
// Example 1
// Input: "abcde"; "ace"
// Output: 3
// Example 2
// Input: "abc"; "abc"
// Output: 3
// Example 3
// Input: "abc"; "def"
// Output: 0

func selfTest() {
	if got := longestCommonSubsequence("abcde", "ace"); !reflect.DeepEqual(got, 3) {
		panic("example 1 failed")
	}
	if got := longestCommonSubsequence("abc", "abc"); !reflect.DeepEqual(got, 3) {
		panic("example 2 failed")
	}
	if got := longestCommonSubsequence("abc", "def"); !reflect.DeepEqual(got, 0) {
		panic("example 3 failed")
	}
}

func selfTestAdditional() {
	// 最小长度边界：单字符且相等 -> 1
	if got := longestCommonSubsequence("a", "a"); !reflect.DeepEqual(got, 1) {
		panic("single equal char failed")
	}
	// 单字符不相等 -> 0
	if got := longestCommonSubsequence("a", "b"); !reflect.DeepEqual(got, 0) {
		panic("single distinct char failed")
	}
	// 顺序敏感：公共字符集是 {a,c,e} 但顺序不允许全部保留，LCS 是 "ae"/"ac" -> 2
	if got := longestCommonSubsequence("abcde", "aec"); !reflect.DeepEqual(got, 2) {
		panic("order-sensitive case failed")
	}
	// 重复字符：结果受较短串的字符数量上限约束 -> 2
	if got := longestCommonSubsequence("aaaa", "aa"); !reflect.DeepEqual(got, 2) {
		panic("repeated char case failed")
	}
	// 完全反序：只能取到单个字符 -> 1
	if got := longestCommonSubsequence("abc", "cba"); !reflect.DeepEqual(got, 1) {
		panic("reversed case failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
