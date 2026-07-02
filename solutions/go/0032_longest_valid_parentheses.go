package main

// Problem: 0032 Longest Valid Parentheses
// URL: https://leetcode.cn/problems/longest-valid-parentheses/
// Difficulty: Hard
// Tags: Stack, String, Dynamic Programming
// Constraints:
// - 0 <= s.length <= 3 * 10^4
// - s[i] is '(', or ')'.

import (
	"reflect"
)

// === Solution ===
func longestValidParentheses1(s string) int {
	if len(s) == 0 {
		return 0
	}
	st := make([]int, 0, len(s))
	st = append(st, -1)
	ans := 0
	for i, _ := range s {
		if s[i] == '(' {
			st = append(st, i)
			continue
		}
		st = st[:len(st)-1]
		if len(st) == 0 {
			st = append(st, i)
			continue
		}
		ans = max(ans, i-st[len(st)-1])
	}
	return ans
}

func at(dp []int, i int) int {
	if i < 0 {
		return 0
	}
	return dp[i]
}
func longestValidParentheses(s string) int {
	if len(s) == 0 {
		return 0
	}
	ans := 0
	dp := make([]int, len(s)+1)
	for i, _ := range dp {
		dp[i] = 0
	}

	for i := 1; i < len(s); i++ {
		if s[i] == '(' {
			continue
		}
		if s[i-1] == '(' {
			dp[i] = at(dp, i-2) + 2
			ans = max(ans, dp[i])
			continue
		}
		pre := i - dp[i-1] - 1 // ()) => 2-2-1 = -1
		if pre >= 0 && s[pre] == '(' {
			dp[i] = dp[i-1] + at(dp, pre-1) + 2
			ans = max(ans, dp[i])
		}
	}

	return ans
}

func longestValidParentheses2(s string) int {
	if len(s) == 0 {
		return 0
	}
	l, r, ans := 0, 0, 0
	for i := 0; i < len(s); i++ {
		if s[i] == '(' {
			l++
		} else {
			r++
		}
		if r == l {
			ans = max(ans, l+r)
		} else if r > l {
			l, r = 0, 0
		}
	}
	l, r = 0, 0
	for i := len(s) - 1; i > -1; i-- {
		if s[i] == ')' {
			r++
		} else {
			l++
		}
		if r == l {
			ans = max(ans, l+r)
		} else if l > r {
			l, r = 0, 0
		}

	}
	return ans
}

// === Test Code ===
// Example 1
// Input: "(()"
// Output: 2
// Example 2
// Input: ")()())"
// Output: 4
// Example 3
// Input: ""
// Output: 0

func selfTest() {
	if got := longestValidParentheses("(()"); !reflect.DeepEqual(got, 2) {
		panic("example 1 failed")
	}
	if got := longestValidParentheses(")()())"); !reflect.DeepEqual(got, 4) {
		panic("example 2 failed")
	}
	if got := longestValidParentheses(""); !reflect.DeepEqual(got, 0) {
		panic("example 3 failed")
	}
}

func selfTestAdditional() {
	// 最小非空输入且无法配对
	if got := longestValidParentheses("("); !reflect.DeepEqual(got, 0) {
		panic("additional test 1 failed")
	}
	// 全是左括号时不存在任何有效连续子串
	if got := longestValidParentheses("((("); !reflect.DeepEqual(got, 0) {
		panic("additional test 2 failed")
	}
	// 整个字符串都是有效括号并包含嵌套
	if got := longestValidParentheses("()(())"); !reflect.DeepEqual(got, 6) {
		panic("additional test 3 failed")
	}
	// 遇到无效断点后，应只统计后面连续有效的最长子串
	if got := longestValidParentheses("())(())"); !reflect.DeepEqual(got, 4) {
		panic("additional test 4 failed")
	}

	if got := longestValidParentheses("()(()"); !reflect.DeepEqual(got, 2) {
		panic("additional test 5 failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
