from __future__ import annotations

# Problem: 1143 Longest Common Subsequence
# URL: https://leetcode.cn/problems/longest-common-subsequence/
# Difficulty: Medium
# Tags: String, Dynamic Programming
# Constraints:
# - 1 <= text1.length, text2.length <= 1000
# - text1 and text2 consist of only lowercase English characters.


# === Solution ===
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i1, c1 in enumerate(text1):
            for i2, c2 in enumerate(text2):
                if c1 == c2:
                    dp[i1 + 1][i2 + 1] = dp[i1][i2] + 1
                else:
                    dp[i1 + 1][i2 + 1] = max(dp[i1][i2 + 1], dp[i1 + 1][i2])

        return dp[m][n]


# === Test Code ===
# Example 1
# Input: "abcde"; "ace"
# Output: 3
# Example 2
# Input: "abc"; "abc"
# Output: 3
# Example 3
# Input: "abc"; "def"
# Output: 0


def _run_examples() -> None:
    solver = Solution()
    assert solver.longestCommonSubsequence("abcde", "ace") == 3, "example 1 failed"
    assert solver.longestCommonSubsequence("abc", "abc") == 3, "example 2 failed"
    assert solver.longestCommonSubsequence("abc", "def") == 0, "example 3 failed"


def _run_additional_tests() -> None:
    solver = Solution()
    # 最小长度边界：单字符且相等 -> 1
    assert solver.longestCommonSubsequence("a", "a") == 1
    # 单字符不相等 -> 0
    assert solver.longestCommonSubsequence("a", "b") == 0
    # 顺序敏感：公共字符集是 {a,c,e} 但顺序不允许全部保留，LCS 是 "ae"/"ac" -> 2
    assert solver.longestCommonSubsequence("abcde", "aec") == 2
    # 重复字符：结果受较短串的字符数量上限约束 -> 2
    assert solver.longestCommonSubsequence("aaaa", "aa") == 2
    # 完全反序：只能取到单个字符 -> 1
    assert solver.longestCommonSubsequence("abc", "cba") == 1


if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
