import pytest

from tests.services.parsers import ResponseParseError, clean_json_block, parse_quiz_response


RAW_QUIZ = """```json
{
  \"questions\": [
    {\"question\": \"Q1\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"correct_index\": 1},
    {\"question\": \"Q2\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"correct_answer\": \"C\"},
    {\"question\": \"Q3\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"answer\": \"D\"}
  ]
}
```"""


def test_clean_json_block_removes_markdown_fences():
    assert clean_json_block("```json\n[1, 2]\n```") == "[1, 2]"


def test_parse_quiz_response_normalizes_three_questions():
    questions = parse_quiz_response(RAW_QUIZ)
    assert len(questions) == 3
    assert [item["correct_index"] for item in questions] == [1, 2, 3]
    assert all(len(item["options"]) == 4 for item in questions)


def test_parse_quiz_requires_exactly_three_questions():
    with pytest.raises(ResponseParseError):
        parse_quiz_response('{"questions": []}')
