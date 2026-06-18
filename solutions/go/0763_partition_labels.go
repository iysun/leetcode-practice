package main

// Problem: 0763 Partition Labels
// URL: https://leetcode.cn/problems/partition-labels/
// Difficulty: Medium
// Tags: Greedy, Hash Table, Two Pointers, String
// Constraints:
// - 1 <= s.length <= 500
// - s consists of lowercase English letters.

// === Solution ===
func partitionLabels(s string) []int {
	last := make(map[byte]int)
	for i := 0; i < len(s); i++ {
		last[s[i]] = i
	}
	res := make([]int, 0)
	start, end := 0, 0
	for i := 0; i < len(s); i++ {
		if last[s[i]] > end {
			end = last[s[i]]
		}
		if i == end {
			res = append(res, end-start+1)
			start = i + 1
		}
	}
	return res
}

// === Test Code ===
// Example 1
// Input: "ababcbacadefegdehijhklij"
// Output: [9,7,8]
// Example 2
// Input: "eccbbbbdec"
// Output: [10]

// Add custom builders for complex structures, then convert the examples above
// into executable assertions.

func selfTestAdditional() {
	// Example 1
	{
		res := partitionLabels("ababcbacadefegdehijhklij")
		expected := []int{9, 7, 8}
		if !equalSlice(res, expected) {
			panic("Example 1 failed")
		}
	}
	// Example 2
	{
		res := partitionLabels("eccbbbbdec")
		expected := []int{10}
		if !equalSlice(res, expected) {
			panic("Example 2 failed")
		}
	}
	// Single character
	{
		res := partitionLabels("a")
		expected := []int{1}
		if !equalSlice(res, expected) {
			panic("Single character failed")
		}
	}
	// All same characters
	{
		res := partitionLabels("aaaaa")
		expected := []int{5}
		if !equalSlice(res, expected) {
			panic("All same characters failed")
		}
	}
	// All distinct characters
	{
		res := partitionLabels("abcdefg")
		expected := []int{1, 1, 1, 1, 1, 1, 1}
		if !equalSlice(res, expected) {
			panic("All distinct characters failed")
		}
	}
	// Two partitions - interleaving
	{
		res := partitionLabels("abac")
		expected := []int{3, 1}
		if !equalSlice(res, expected) {
			panic("Interleaving failed")
		}
	}
	// Each char appears at most once - every char is its own partition
	{
		res := partitionLabels("zyxwvutsrqponmlkjihgfedcba")
		expected := make([]int, 26)
		for i := range expected {
			expected[i] = 1
		}
		if !equalSlice(res, expected) {
			panic("All unique characters failed")
		}
	}
	// Maximum length string with all 'a' - single partition
	{
		s := make([]byte, 500)
		for i := range s {
			s[i] = 'a'
		}
		res := partitionLabels(string(s))
		expected := []int{500}
		if !equalSlice(res, expected) {
			panic("All 'a' at max length failed")
		}
	}

	println("All additional tests passed!")
}

func equalSlice(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func main() {
	selfTestAdditional()
}
