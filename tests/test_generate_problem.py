from __future__ import annotations

import unittest

from scripts.generate_problem import (
    ExampleCase,
    GenerationError,
    build_metadata,
    can_render_executable_examples,
    extract_constraints,
    extract_examples,
    fill_go_stub,
    fill_python_stub,
    parse_meta,
    render_go_file,
    render_python_file,
)


QUESTION = {
    "title": "Two Sum",
    "titleSlug": "two-sum",
    "difficulty": "Easy",
    "content": """
<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return indices of the two numbers such that they add up to <code>target</code>.</p>
<p><strong class="example">Example 1:</strong></p>
<pre>
<strong>Input:</strong> nums = [2,7,11,15], target = 9
<strong>Output:</strong> [0,1]
</pre>
<p><strong class="example">Example 2:</strong></p>
<pre>
<strong>Input:</strong> nums = [3,2,4], target = 6
<strong>Output:</strong> [1,2]
</pre>
<p><strong>Constraints:</strong></p>
<ul>
    <li><code>2 <= nums.length <= 10^4</code></li>
    <li><code>-10^9 <= nums[i] <= 10^9</code></li>
</ul>
""".strip(),
    "topicTags": [{"name": "Array"}, {"name": "Hash Table"}],
    "jsonExampleTestcases": '["[2,7,11,15]\\n9", "[3,2,4]\\n6"]',
    "codeSnippets": [
        {
            "langSlug": "python3",
            "code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        \n",
        },
        {
            "langSlug": "golang",
            "code": "func twoSum(nums []int, target int) []int {\n    \n}\n",
        },
    ],
}


META = parse_meta(
    """
{
  "name": "twoSum",
  "params": [
    {"name": "nums", "type": "integer[]"},
    {"name": "target", "type": "integer"}
  ],
  "return": {"type": "integer[]", "size": 2},
  "manual": false
}
""".strip()
)


class GenerateProblemTests(unittest.TestCase):
    def test_extract_examples(self) -> None:
        examples = extract_examples(QUESTION)
        self.assertEqual(
            examples,
            [
                ExampleCase(raw_input="[2,7,11,15]\n9", raw_output="[0,1]"),
                ExampleCase(raw_input="[3,2,4]\n6", raw_output="[1,2]"),
            ],
        )

    def test_extract_constraints(self) -> None:
        self.assertEqual(
            extract_constraints(QUESTION["content"]),
            ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        )

    def test_fill_python_stub_inserts_not_implemented(self) -> None:
        rendered = fill_python_stub(QUESTION["codeSnippets"][0]["code"])
        self.assertIn("raise NotImplementedError", rendered)

    def test_fill_go_stub_inserts_todo_panic(self) -> None:
        rendered = fill_go_stub(QUESTION["codeSnippets"][1]["code"])
        self.assertIn('panic("TODO: implement")', rendered)

    def test_examples_are_executable_for_primitive_signatures(self) -> None:
        examples = extract_examples(QUESTION)
        self.assertTrue(can_render_executable_examples(META, examples))

    def test_examples_are_not_executable_for_list_node_signatures(self) -> None:
        list_node_meta = parse_meta(
            """
{
  "name": "reverseList",
  "params": [{"name": "head", "type": "ListNode"}],
  "return": {"type": "ListNode", "dealloc": true}
}
""".strip()
        )
        examples = [ExampleCase(raw_input="[1,2,3,4,5]", raw_output="[5,4,3,2,1]")]
        self.assertFalse(can_render_executable_examples(list_node_meta, examples))

    def test_render_python_file_contains_solution_and_test_sections(self) -> None:
        examples = extract_examples(QUESTION)
        rendered = render_python_file(QUESTION, META, examples, "0001")
        self.assertIn("# === Solution ===", rendered)
        self.assertIn("# === Test Code ===", rendered)
        self.assertIn("assert solver.twoSum", rendered)
        self.assertIn("def _run_additional_tests() -> None:", rendered)

    def test_render_go_file_contains_solution_and_test_sections(self) -> None:
        examples = extract_examples(QUESTION)
        rendered = render_go_file(QUESTION, META, examples, "0001")
        self.assertIn("// === Solution ===", rendered)
        self.assertIn("// === Test Code ===", rendered)
        self.assertIn("reflect.DeepEqual", rendered)
        self.assertIn("func selfTestAdditional()", rendered)

    def test_parse_meta_rejects_missing_payload(self) -> None:
        with self.assertRaises(GenerationError):
            parse_meta(None)

    def test_build_metadata_contains_statement_and_hints(self) -> None:
        question = dict(QUESTION)
        question["translatedTitle"] = "两数之和"
        question["translatedContent"] = "<p>给定数组和目标值。</p>"
        question["sampleTestCase"] = "[2,7,11,15]\\n9"
        question["hints"] = ["<p>Try a hash map.</p>"]
        metadata = build_metadata(question, META, extract_examples(question))
        self.assertEqual(metadata["translated_title"], "两数之和")
        self.assertIn("Given an array", metadata["statement_text"])
        self.assertEqual(metadata["translated_statement_text"], "给定数组和目标值。")
        self.assertEqual(metadata["sample_test_case"], "[2,7,11,15]\\n9")
        self.assertEqual(metadata["hints"], ["Try a hash map."])


if __name__ == "__main__":
    unittest.main()
