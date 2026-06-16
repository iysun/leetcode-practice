from __future__ import annotations

import argparse
import ast
import html
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROBLEMSET_API_URL = "https://leetcode.com/api/problems/all/"
QUESTION_PAGE_URL = "https://leetcode.cn/problems/{slug}/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
REPO_ROOT = Path(__file__).resolve().parents[1]


class GenerationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProblemSummary:
    frontend_id: str
    title: str
    title_slug: str


@dataclass(frozen=True)
class ExampleCase:
    raw_input: str
    raw_output: str


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(fetch_text(url))


def load_problem_index() -> dict[str, ProblemSummary]:
    payload = fetch_json(PROBLEMSET_API_URL)
    problems: dict[str, ProblemSummary] = {}
    for item in payload.get("stat_status_pairs", []):
        stat = item.get("stat", {})
        frontend_id = str(stat.get("frontend_question_id", "")).strip()
        title_slug = stat.get("question__title_slug")
        title = stat.get("question__title")
        if not frontend_id or not title_slug or not title:
            continue
        problems[frontend_id] = ProblemSummary(
            frontend_id=frontend_id,
            title=title,
            title_slug=title_slug,
        )
    return problems


def fetch_question_detail(title_slug: str) -> dict[str, Any]:
    page_html = fetch_text(QUESTION_PAGE_URL.format(slug=title_slug))
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        page_html,
        re.S,
    )
    if not match:
        raise GenerationError("Unable to find __NEXT_DATA__ payload in question page.")

    next_data = json.loads(match.group(1))
    for query in next_data.get("props", {}).get("pageProps", {}).get("dehydratedState", {}).get(
        "queries", []
    ):
        query_key = query.get("queryKey")
        if not query_key or query_key[0] != "questionDetail":
            continue
        question = query.get("state", {}).get("data", {}).get("question")
        if question:
            return question
    raise GenerationError("Unable to find question detail payload in page data.")


def normalize_problem_prefix(problem_id: str) -> str:
    try:
        return f"{int(problem_id):04d}"
    except ValueError as exc:
        raise GenerationError(f"Invalid problem id: {problem_id}") from exc


def parse_meta(meta_data_raw: str | None) -> dict[str, Any]:
    if not meta_data_raw:
        raise GenerationError("Question metadata is missing.")
    return json.loads(meta_data_raw.replace("\r", ""))


def strip_html_tags(raw_html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", raw_html)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", text)
    text = re.sub(r"</?[A-Za-z][^>]*>", "", text)
    return html.unescape(text).replace("\xa0", " ").strip()


def extract_example_outputs(content_html: str) -> list[str]:
    outputs: list[str] = []
    for block in re.findall(r"<pre>(.*?)</pre>", content_html, re.S):
        block_text = strip_html_tags(block)
        match = re.search(r"Output:\s*(.+)", block_text)
        if match:
            outputs.append(match.group(1).strip())
    return outputs


def extract_constraints(content_html: str) -> list[str]:
    match = re.search(r"<strong>Constraints:</strong>(.*?)</ul>", content_html, re.S)
    if not match:
        return []
    section = match.group(1)
    return [strip_html_tags(item) for item in re.findall(r"<li>(.*?)</li>", section, re.S)]


def extract_hints(hints: list[str] | None) -> list[str]:
    if not hints:
        return []
    return [strip_html_tags(item) for item in hints if strip_html_tags(item)]


def extract_examples(question: dict[str, Any]) -> list[ExampleCase]:
    raw_examples = question.get("jsonExampleTestcases")
    if raw_examples:
        input_cases = json.loads(raw_examples)
    else:
        raw_text = question.get("exampleTestcases", "")
        chunks = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]
        input_cases = chunks

    outputs = extract_example_outputs(question.get("content", ""))
    case_count = min(len(input_cases), len(outputs))
    return [
        ExampleCase(raw_input=input_cases[index].strip(), raw_output=outputs[index].strip())
        for index in range(case_count)
    ]


def canonicalize_literal(raw_value: str) -> str:
    return re.sub(r"\btrue\b", "True", re.sub(r"\bfalse\b", "False", re.sub(r"\bnull\b", "None", raw_value)))


def parse_python_literal(raw_value: str) -> Any:
    try:
        return ast.literal_eval(canonicalize_literal(raw_value))
    except (SyntaxError, ValueError) as exc:
        raise GenerationError(f"Unsupported literal value: {raw_value}") from exc


def is_supported_literal(meta_type: str) -> bool:
    if meta_type.endswith("[]"):
        return is_supported_literal(meta_type[:-2])
    return meta_type in {"integer", "double", "string", "boolean"}


def python_expr(raw_value: str) -> str:
    parsed = parse_python_literal(raw_value)
    return repr(parsed)


def go_type(meta_type: str) -> str:
    if meta_type.endswith("[]"):
        return "[]" + go_type(meta_type[:-2])
    mapping = {
        "integer": "int",
        "double": "float64",
        "string": "string",
        "boolean": "bool",
    }
    if meta_type not in mapping:
        raise GenerationError(f"Unsupported Go type for literal rendering: {meta_type}")
    return mapping[meta_type]


def go_expr(raw_value: str, meta_type: str) -> str:
    parsed = parse_python_literal(raw_value)
    return go_literal(parsed, meta_type)


def go_literal(value: Any, meta_type: str) -> str:
    if meta_type.endswith("[]"):
        if not isinstance(value, list):
            raise GenerationError(f"Expected list value for Go type {meta_type}.")
        child_type = meta_type[:-2]
        rendered = ", ".join(go_literal(item, child_type) for item in value)
        return f"{go_type(meta_type)}{{{rendered}}}"

    if meta_type == "integer":
        return str(value)
    if meta_type == "double":
        return repr(float(value))
    if meta_type == "string":
        return json.dumps(value)
    if meta_type == "boolean":
        return "true" if value else "false"
    raise GenerationError(f"Unsupported Go type for literal rendering: {meta_type}")


def can_render_executable_examples(meta: dict[str, Any], examples: list[ExampleCase]) -> bool:
    if not examples:
        return False
    params = meta.get("params", [])
    return_type = meta.get("return", {}).get("type", "")
    if not return_type or not is_supported_literal(return_type):
        return False
    for param in params:
        if not is_supported_literal(param.get("type", "")):
            return False
    for example in examples:
        raw_values = [line.strip() for line in example.raw_input.splitlines() if line.strip()]
        if len(raw_values) != len(params):
            return False
        try:
            for raw_value, param in zip(raw_values, params):
                python_expr(raw_value)
                go_expr(raw_value, param["type"])
            python_expr(example.raw_output)
            go_expr(example.raw_output, return_type)
        except GenerationError:
            return False
    return True


def render_problem_header(prefix: str, question: dict[str, Any]) -> list[str]:
    tags = ", ".join(tag.get("name", "") for tag in question.get("topicTags", []) if tag.get("name"))
    header = [
        f"Problem: {prefix} {question.get('title', '')}",
        f"URL: {QUESTION_PAGE_URL.format(slug=question.get('titleSlug', ''))}",
        f"Difficulty: {question.get('difficulty', '')}",
    ]
    if tags:
        header.append(f"Tags: {tags}")
    return header


def fill_python_stub(code: str) -> str:
    stripped = code.rstrip()
    lines = stripped.splitlines()
    if not lines:
        raise GenerationError("Empty Python template.")

    last_index = len(lines) - 1
    while last_index >= 0 and not lines[last_index].strip():
        last_index -= 1
    if last_index < 0:
        raise GenerationError("Invalid Python template.")
    if lines[last_index].rstrip().endswith(":"):
        indent = len(lines[last_index]) - len(lines[last_index].lstrip()) + 4
        lines = lines[: last_index + 1] + [" " * indent + "raise NotImplementedError"]
    return "\n".join(lines)


def required_python_typing_imports(code: str) -> list[str]:
    imports: list[str] = []
    for name in ("Dict", "List", "Optional", "Set", "Tuple"):
        if re.search(rf"\b{name}\b", code):
            imports.append(name)
    return imports


def render_python_example_runner(
    meta: dict[str, Any],
    examples: list[ExampleCase],
) -> str:
    lines = ["def _run_examples() -> None:", "    solver = Solution()"]
    method_name = meta["name"]
    for index, example in enumerate(examples, start=1):
        raw_values = [line.strip() for line in example.raw_input.splitlines() if line.strip()]
        arguments = ", ".join(python_expr(raw_value) for raw_value in raw_values)
        expected = python_expr(example.raw_output)
        lines.append(
            f"    assert solver.{method_name}({arguments}) == {expected}, "
            f"\"example {index} failed\""
        )
    return "\n".join(lines)


def render_python_additional_test_runner() -> str:
    return "\n".join(
        [
            "def _run_additional_tests() -> None:",
            "    # Add boundary cases and special-case assertions after reviewing",
            "    # the generated file together with problems/<id>_<slug>.json.",
            "    pass",
        ]
    )


def render_python_file(
    question: dict[str, Any],
    meta: dict[str, Any],
    examples: list[ExampleCase],
    prefix: str,
) -> str:
    template = next(
        (item["code"] for item in question.get("codeSnippets", []) if item.get("langSlug") == "python3"),
        None,
    )
    if not template:
        raise GenerationError("Python template is missing from question data.")

    solution_code = fill_python_stub(template)
    header_lines = [f"# {line}" for line in render_problem_header(prefix, question)]
    constraints = extract_constraints(question.get("content", ""))
    if constraints:
        header_lines.append("# Constraints:")
        header_lines.extend(f"# - {constraint}" for constraint in constraints)

    sections: list[str] = ["from __future__ import annotations"]
    typing_imports = required_python_typing_imports(solution_code)
    if typing_imports:
        sections.append(f"from typing import {', '.join(typing_imports)}")
    sections.extend(["", *header_lines, "", "# === Solution ===", solution_code, "", "# === Test Code ==="])

    for index, example in enumerate(examples, start=1):
        sections.extend(
            [
                f"# Example {index}",
                f"# Input: {example.raw_input.replace(chr(10), '; ')}",
                f"# Output: {example.raw_output}",
            ]
        )

    sections.append("")
    if can_render_executable_examples(meta, examples):
        sections.append(render_python_example_runner(meta, examples))
        sections.extend(
            [
                "",
                render_python_additional_test_runner(),
                "",
                'if __name__ == "__main__":',
                "    _run_examples()",
                "    _run_additional_tests()",
            ]
        )
    else:
        sections.extend(
            [
                "# Add custom builders for complex structures, then convert the examples above",
                "# into executable assertions.",
                "",
                render_python_additional_test_runner(),
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def fill_go_stub(code: str) -> str:
    stripped = code.rstrip()
    replaced = re.sub(
        r"\{\s*\}\s*$",
        '{\n\tpanic("TODO: implement")\n}',
        stripped,
        flags=re.S,
    )
    if replaced == stripped:
        return stripped
    return replaced


def render_go_example_runner(
    meta: dict[str, Any],
    examples: list[ExampleCase],
) -> str:
    method_name = meta["name"]
    params = meta["params"]
    return_type = meta["return"]["type"]
    lines = ["func selfTest() {"]
    for index, example in enumerate(examples, start=1):
        raw_values = [line.strip() for line in example.raw_input.splitlines() if line.strip()]
        arguments = ", ".join(
            go_expr(raw_value, param["type"]) for raw_value, param in zip(raw_values, params)
        )
        expected = go_expr(example.raw_output, return_type)
        lines.extend(
            [
                f"\tif got := {method_name}({arguments}); !reflect.DeepEqual(got, {expected}) {{",
                f'\t\tpanic("example {index} failed")',
                "\t}",
            ]
        )
    lines.append("}")
    return "\n".join(lines)


def render_go_additional_test_runner() -> str:
    return "\n".join(
        [
            "func selfTestAdditional() {",
            "\t// Add boundary cases and special-case assertions after reviewing",
            "\t// the generated file together with problems/<id>_<slug>.json.",
            "}",
        ]
    )


def render_go_file(
    question: dict[str, Any],
    meta: dict[str, Any],
    examples: list[ExampleCase],
    prefix: str,
) -> str:
    template = next(
        (item["code"] for item in question.get("codeSnippets", []) if item.get("langSlug") == "golang"),
        None,
    )
    if not template:
        raise GenerationError("Go template is missing from question data.")

    solution_code = fill_go_stub(template)
    comment_lines = [f"// {line}" for line in render_problem_header(prefix, question)]
    constraints = extract_constraints(question.get("content", ""))
    if constraints:
        comment_lines.append("// Constraints:")
        comment_lines.extend(f"// - {constraint}" for constraint in constraints)

    sections = ["package main", "", *comment_lines]
    executable = can_render_executable_examples(meta, examples)
    if executable:
        sections.extend(["", 'import "reflect"'])
    sections.extend(["", "// === Solution ===", solution_code, "", "// === Test Code ==="])

    for index, example in enumerate(examples, start=1):
        sections.extend(
            [
                f"// Example {index}",
                f"// Input: {example.raw_input.replace(chr(10), '; ')}",
                f"// Output: {example.raw_output}",
            ]
        )

    sections.append("")
    if executable:
        sections.extend(
            [
                render_go_example_runner(meta, examples),
                "",
                render_go_additional_test_runner(),
            ]
        )
    else:
        sections.extend(
            [
                "// Add custom builders for complex structures, then convert the examples above",
                "// into executable assertions.",
                "",
                render_go_additional_test_runner(),
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def build_metadata(
    question: dict[str, Any],
    meta: dict[str, Any],
    examples: list[ExampleCase],
) -> dict[str, Any]:
    return {
        "id": question.get("questionFrontendId") or question.get("questionId"),
        "title": question.get("title"),
        "translated_title": question.get("translatedTitle"),
        "title_slug": question.get("titleSlug"),
        "url": QUESTION_PAGE_URL.format(slug=question.get("titleSlug", "")),
        "difficulty": question.get("difficulty"),
        "statement_text": strip_html_tags(question.get("content", "")),
        "translated_statement_text": strip_html_tags(question.get("translatedContent", "")),
        "tags": [tag.get("name") for tag in question.get("topicTags", []) if tag.get("name")],
        "signature": {
            "name": meta.get("name"),
            "params": meta.get("params", []),
            "return": meta.get("return", {}),
        },
        "sample_test_case": question.get("sampleTestCase"),
        "examples": [
            {"input": example.raw_input, "output": example.raw_output} for example in examples
        ],
        "constraints": extract_constraints(question.get("content", "")),
        "hints": extract_hints(question.get("hints")),
    }


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise GenerationError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate(problem_id: str, languages: set[str], force: bool) -> list[Path]:
    try:
        normalized_id = str(int(problem_id))
    except ValueError as exc:
        raise GenerationError(f"Invalid problem id: {problem_id}") from exc

    problem_index = load_problem_index()
    summary = problem_index.get(normalized_id)
    if not summary:
        raise GenerationError(f"Problem id {problem_id} was not found in the problem list.")

    question = fetch_question_detail(summary.title_slug)
    meta = parse_meta(question.get("metaData"))
    examples = extract_examples(question)
    prefix = normalize_problem_prefix(problem_id)
    stem = f"{prefix}_{summary.title_slug.replace('-', '_')}"

    outputs: list[tuple[Path, str]] = []
    metadata_path = REPO_ROOT / "problems" / f"{stem}.json"
    metadata_content = json.dumps(build_metadata(question, meta, examples), ensure_ascii=False, indent=2) + "\n"
    outputs.append((metadata_path, metadata_content))

    if "py" in languages:
        python_path = REPO_ROOT / "solutions" / "py" / f"{stem}.py"
        outputs.append((python_path, render_python_file(question, meta, examples, prefix)))

    if "go" in languages:
        go_path = REPO_ROOT / "solutions" / "go" / f"{stem}.go"
        outputs.append((go_path, render_go_file(question, meta, examples, prefix)))

    if not force:
        for path, _ in outputs:
            if path.exists():
                raise GenerationError(f"Refusing to overwrite existing file: {path}")

    for path, content in outputs:
        write_file(path, content, force=force)

    return [path for path, _ in outputs]


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate single-file Python and Go LeetCode templates from a problem id."
    )
    parser.add_argument("problem_id", help="LeetCode frontend problem id, for example 1")
    parser.add_argument(
        "--lang",
        dest="languages",
        action="append",
        choices=("py", "go"),
        help="Restrict generation to one or more languages. Defaults to both.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_arguments(argv or sys.argv[1:])
    languages = set(args.languages or ["py", "go"])
    try:
        created_paths = generate(args.problem_id, languages, force=args.force)
    except GenerationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for path in created_paths:
        print(path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
