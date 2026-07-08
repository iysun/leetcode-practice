from __future__ import annotations

# Problem: 0005 Longest Palindromic Substring
# URL: https://leetcode.cn/problems/longest-palindromic-substring/
# Difficulty: Medium
# Tags: Two Pointers, String, Dynamic Programming
# Constraints:
# - 1 <= s.length <= 1000
# - s consist of only digits and English letters.


# === Solution ===
class Solution:
    # Manacher算法（马拉车）最优算法 time: O(n) space: O(n)
    def longestPalindrome(self, s: str) -> str:
        T = "^#" + "#".join(s) + "#$"
        n = len(T)
        P = [0] * n

        C = 0
        R = 0

        for i in range(1, n - 1):
            mirror_i = 2 * C - i
            if i < R:
                P[i] = min(P[mirror_i], R - i)

            while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
                P[i] += 1

            if i + P[i] > R:
                C = i
                R = i + P[i]
        max_radius = max(P)
        center_index = P.index(max_radius)

        start = (center_index - max_radius) // 2
        return s[start : start + max_radius]

    # 动态规划 time: O(n^2) space: O(n^2)
    # def longestPalindrome(self, s: str) -> str:
    #     n = len(s)
    #     dp = [[False] * n for _ in range(n)]
    #     max_len = 1
    #     start = 0
    #     for i in range(0, n):
    #         dp[i][i] = True
    #     for length in range(2, n + 1):
    #         for i in range(n - length + 1):
    #             j = i + length - 1

    #             if s[i] != s[j]:
    #                 dp[i][j] = False
    #             else:
    #                 if length == 2:
    #                     dp[i][j] = True
    #                 else:
    #                     dp[i][j] = dp[i + 1][j - 1]
    #             if dp[i][j] and length > max_len:
    #                 max_len = length
    #                 start = i
    #     return s[start : start + max_len]

    # 中心扩散 time: O(n^2) space: O(1)
    # def longestPalindrome(self, s: str) -> str:
    #     length = 1
    #     ans = s[0:1]
    #     n = len(s)
    #     for r in range(1, n):
    #         for l in [r, r-1]:
    #             j,i = l,r
    #             while j >= 0 and i < n:
    #                 if s[i] != s[j]:
    #                     break
    #                 if i - j + 1 > length:
    #                     length = i - j + 1
    #                     ans = s[j : i + 1]

    #                 j -= 1
    #                 i += 1
    #     return ans


# === Test Code ===
# Example 1
# Input: "babad"
# Output: "bab"
# Example 2
# Input: "cbbd"
# Output: "bb"


def _run_examples() -> None:
    solver = Solution()
    assert solver.longestPalindrome("babad") == "bab", "example 1 failed"
    assert solver.longestPalindrome("cbbd") == "bb", "example 2 failed"


def _run_additional_tests() -> None:
    # err
    assert Solution().longestPalindrome("abbcccba") == "bcccb"
    # 单字符输入，答案唯一
    assert Solution().longestPalindrome("a") == "a"
    # 全部同字符，最长回文即整串，长度唯一不存在并列
    assert Solution().longestPalindrome("aaaa") == "aaaa"
    # 偶数长度且整串即为回文
    assert Solution().longestPalindrome("abba") == "abba"
    # 回文子串不在开头，且长度唯一最长（避免并列答案的歧义）
    assert Solution().longestPalindrome("xaba") == "aba"
    # 数字输入，偶数长度回文
    assert Solution().longestPalindrome("1221") == "1221"


if __name__ == "__main__":
    _run_examples()
    _run_additional_tests()
