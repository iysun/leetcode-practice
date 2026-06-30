package main

import "slices"

// Problem: 0139 Word Break
// URL: https://leetcode.cn/problems/word-break/
// Difficulty: Medium
// Tags: Trie, Memoization, Array, Hash Table, String, Dynamic Programming
// Constraints:
// - 1 <= s.length <= 300
// - 1 <= wordDict.length <= 1000
// - 1 <= wordDict[i].length <= 20
// - s and wordDict[i] consist of only lowercase English letters.
// - All the strings of wordDict are unique.

// === Solution ===
func wordBreak(s string, wordDict []string) bool {
	n := len(s)
	dp := make([]bool, n+1)
	for i, _ := range dp {
		dp[i] = false
	}
	dp[0] = true
	for i := 0; i < n+1; i++ {
		for j := 0; j < i; j++ {
			word := s[j:i]
			if slices.Contains(wordDict, word) && dp[j] {
				dp[i] = true
			}
		}
	}
	return dp[n]
}

// === Test Code ===
// Example 1
// Input: "leetcode"; ["leet","code"]
// Output: true
// Example 2
// Input: "applepenapple"; ["apple","pen"]
// Output: true
// Example 3
// Input: "catsandog"; ["cats","dog","sand","and","cat"]
// Output: false

func selfTestExamples() {
	// Example 1
	if !wordBreak("leetcode", []string{"leet", "code"}) {
		panic("example 1 failed")
	}
	// Example 2
	if !wordBreak("applepenapple", []string{"apple", "pen"}) {
		panic("example 2 failed")
	}
	// Example 3
	if wordBreak("catsandog", []string{"cats", "dog", "sand", "and", "cat"}) {
		panic("example 3 failed")
	}
}

func selfTestAdditional() {
	// Single character, in dict
	if !wordBreak("a", []string{"a"}) {
		panic("test 1 failed")
	}
	// Single character, not in dict
	if wordBreak("a", []string{"b"}) {
		panic("test 2 failed")
	}
	// Reuse same word multiple times
	if !wordBreak("aaaa", []string{"a"}) {
		panic("test 3 failed")
	}
	// Overlapping words — no valid segmentation exists
	if wordBreak("abc", []string{"ab", "bc"}) {
		panic("test 4 failed")
	}
	// Match via non‑greedy path
	if wordBreak("abcd", []string{"a", "abc", "cd"}) {
		panic("test 5 failed")
	}
}

func main() {
	selfTestExamples()
	selfTestAdditional()
}
