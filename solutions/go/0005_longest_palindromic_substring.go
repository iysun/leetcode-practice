package main

// Problem: 0005 Longest Palindromic Substring
// URL: https://leetcode.cn/problems/longest-palindromic-substring/
// Difficulty: Medium
// Tags: Two Pointers, String, Dynamic Programming
// Constraints:
// - 1 <= s.length <= 1000
// - s consist of only digits and English letters.

import "reflect"

// === Solution ===
func longestPalindrome(s string) string {
	max_len := 1
	start := 0
	n := len(s)
	for r := 1; r < n; r++ {
		for _, l := range []int{r, r - 1} {
			j, i := l, r
			for j >= 0 && i < n {
				if s[i] != s[j] {
					break
				}
				if i-j+1 > max_len {
					max_len = i - j + 1
					start = j
				}
				j--
				i++
			}
		}
	}
	return s[start : start+max_len]
}

// === Test Code ===
// Example 1
// Input: "babad"
// Output: "bab"
// Example 2
// Input: "cbbd"
// Output: "bb"

func selfTest() {
	if got := longestPalindrome("babad"); !reflect.DeepEqual(got, "bab") {
		panic("example 1 failed")
	}
	if got := longestPalindrome("cbbd"); !reflect.DeepEqual(got, "bb") {
		panic("example 2 failed")
	}
}

func selfTestAdditional() {
	// 单字符输入，答案唯一
	if got := longestPalindrome("a"); !reflect.DeepEqual(got, "a") {
		panic("single char failed")
	}
	// 全部同字符，最长回文即整串，长度唯一不存在并列
	if got := longestPalindrome("aaaa"); !reflect.DeepEqual(got, "aaaa") {
		panic("all same chars failed")
	}
	// 偶数长度且整串即为回文
	if got := longestPalindrome("abba"); !reflect.DeepEqual(got, "abba") {
		panic("whole string even palindrome failed")
	}
	// 回文子串不在开头，且长度唯一最长（避免并列答案的歧义）
	if got := longestPalindrome("xaba"); !reflect.DeepEqual(got, "aba") {
		panic("embedded unique-longest palindrome failed")
	}
	// 数字输入，偶数长度回文
	if got := longestPalindrome("1221"); !reflect.DeepEqual(got, "1221") {
		panic("digit palindrome failed")
	}
}

func main() {
	selfTest()
	selfTestAdditional()
}
