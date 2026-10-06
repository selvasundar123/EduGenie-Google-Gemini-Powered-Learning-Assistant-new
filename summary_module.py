from tests.services.gemini_client import GeminiClient
from tests.services.prompts import summary_prompt


def summarize_text(text: str, client: GeminiClient | None = None) -> str:
    return (client or GeminiClient()).generate(summary_prompt(text))
