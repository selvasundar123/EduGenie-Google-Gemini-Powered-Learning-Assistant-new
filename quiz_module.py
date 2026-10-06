from tests.services.gemini_client import GeminiClient
from tests.services.parsers import parse_quiz_response
from tests.services.prompts import quiz_prompt


def generate_quiz(text: str, client: GeminiClient | None = None) -> list[dict]:
    model_client = client or GeminiClient()
    raw = model_client.generate(quiz_prompt(text), json_mode=True)
    return parse_quiz_response(raw)
