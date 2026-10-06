import json
import re
from typing import Any


class ResponseParseError(ValueError):
    """Raised when a model response cannot be converted to the expected shape."""


def clean_json_block(raw: str) -> str:
    """Remove Markdown fences and isolate the first JSON object or array."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    starts = [index for index in (text.find("["), text.find("{")) if index >= 0]
    if not starts:
        raise ResponseParseError("Gemini did not return a JSON object or array.")
    start = min(starts)
    end_array = text.rfind("]")
    end_object = text.rfind("}")
    end = max(end_array, end_object)
    if end < start:
        raise ResponseParseError("Gemini returned incomplete JSON.")
    return text[start : end + 1]


def _correct_index(item: dict[str, Any], options: list[str]) -> int:
    if isinstance(item.get("correct_index"), int):
        return item["correct_index"]
    if isinstance(item.get("answer_index"), int):
        return item["answer_index"]
    answer = item.get("correct_answer", item.get("answer"))
    if isinstance(answer, int):
        return answer
    if isinstance(answer, str):
        normalized = answer.strip()
        if len(normalized) == 1 and normalized.upper() in "ABCD":
            return "ABCD".index(normalized.upper())
        for index, option in enumerate(options):
            if normalized.casefold() == option.strip().casefold():
                return index
    raise ResponseParseError("Each quiz question needs a valid correct answer.")


def parse_quiz_response(raw: str) -> list[dict[str, Any]]:
    payload = json.loads(clean_json_block(raw))
    questions = payload.get("questions") if isinstance(payload, dict) else payload
    if not isinstance(questions, list) or len(questions) != 3:
        raise ResponseParseError("Gemini must return exactly three quiz questions.")

    normalized: list[dict[str, Any]] = []
    for item in questions:
        if not isinstance(item, dict):
            raise ResponseParseError("Every quiz question must be an object.")
        question = str(item.get("question", "")).strip()
        options = item.get("options")
        if not question or not isinstance(options, list) or len(options) != 4:
            raise ResponseParseError("Each quiz question needs text and exactly four options.")
        options = [str(option).strip() for option in options]
        correct_index = _correct_index(item, options)
        if correct_index not in range(4):
            raise ResponseParseError("Correct answer index must be between 0 and 3.")
        normalized.append(
            {
                "question": question,
                "options": options,
                "correct_index": correct_index,
                "explanation": str(item.get("explanation", "")).strip(),
            }
        )
    return normalized
