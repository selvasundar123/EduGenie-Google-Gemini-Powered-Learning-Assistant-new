from tests.services.gemini_client import GeminiClient
from tests.services.prompts import qa_prompt


def answer_question(question: str, client: GeminiClient | None = None) -> str:
    return (client or GeminiClient()).generate(qa_prompt(question))
