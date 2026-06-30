from __future__ import annotations
from typing import List

# Problem: 0139 Word Break
# URL: https://leetcode.cn/problems/word-break/
# Difficulty: Medium
# Tags: Trie, Memoization, Array, Hash Table, String, Dynamic Programming
# Constraints:
# - 1 <= s.length <= 300
# - 1 <= wordDict.length <= 1000
# - 1 <= wordDict[i].length <= 20
# - s and wordDict[i] consist of only lowercase English letters.
# - All the strings of wordDict are unique.

# === Solution ===
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        dp = [False] * (n+1)
        dp[0] = True
        for i in range(0, n+1):
            if not dp[i]: continue
            for word in wordDict:
                if i + len(word) <= n and s[i:i+len(word)] == word:
                    dp[i+len(word)] = True
        return dp[-1]



# === Test Code ===
# Example 1
# Input: "leetcode"; ["leet","code"]
# Output: true
# Example 2
# Input: "applepenapple"; ["apple","pen"]
# Output: true
# Example 3
# Input: "catsandog"; ["cats","dog","sand","and","cat"]
# Output: false

def _run_examples() -> None:
    solver = Solution()
    assert solver.wordBreak("leetcode", ["leet", "code"]) is True, "example 1 failed"
    assert solver.wordBreak("applepenapple", ["apple", "pen"]) is True, "example 2 failed"
    assert solver.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False, "example 3 failed"

def _run_additional_tests() -> None:
    # Single character, in dict
    assert Solution().wordBreak("a", ["a"]) is True
    # Single character, not in dict
    assert Solution().wordBreak("a", ["b"]) is False
    # Reuse same word multiple times
    assert Solution().wordBreak("aaaa", ["a"]) is True
    # Overlapping words — no valid segmentation exists
    assert Solution().wordBreak("abc", ["ab", "bc"]) is False
    # Match via non‑greedy path
    assert Solution().wordBreak("abcd", ["a", "abc", "cd"]) is False

if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
