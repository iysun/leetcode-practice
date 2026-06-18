from __future__ import annotations
from typing import List

# Problem: 0763 Partition Labels
# URL: https://leetcode.cn/problems/partition-labels/
# Difficulty: Medium
# Tags: Greedy, Hash Table, Two Pointers, String
# Constraints:
# - 1 <= s.length <= 500
# - s consists of lowercase English letters.

# === Solution ===
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {c: i for i, c in enumerate(s)}
        res = []
        start = end = 0
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                res.append(end - start + 1)
                start = i + 1
        return res

# === Test Code ===
# Example 1
# Input: "ababcbacadefegdehijhklij"
# Output: [9,7,8]
# Example 2
# Input: "eccbbbbdec"
# Output: [10]

# Add custom builders for complex structures, then convert the examples above
# into executable assertions.

def _run_additional_tests() -> None:
    sol = Solution()

    # Example 1
    assert sol.partitionLabels("ababcbacadefegdehijhklij") == [9, 7, 8]
    # Example 2
    assert sol.partitionLabels("eccbbbbdec") == [10]

    # Single character
    assert sol.partitionLabels("a") == [1]

    # All same characters
    assert sol.partitionLabels("aaaaa") == [5]

    # All distinct characters
    assert sol.partitionLabels("abcdefg") == [1, 1, 1, 1, 1, 1, 1]

    # Two partitions - interleaving
    assert sol.partitionLabels("abac") == [3, 1]

    # Each char appears at most once - every char is its own partition
    assert sol.partitionLabels("zyxwvutsrqponmlkjihgfedcba") == [1] * 26

    # Maximum length string with all 'a' - single partition
    assert sol.partitionLabels("a" * 500) == [500]

    print("All additional tests passed!")
