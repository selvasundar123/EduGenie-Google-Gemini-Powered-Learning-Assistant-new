from tests.services.gemini_client import GeminiClient
from tests.services.prompts import explain_prompt


def explain_concept(topic: str, client: GeminiClient | None = None) -> str:
    """Explain a concept. The optional local LaMini model can be added here later.

    The first version intentionally keeps local model downloads optional and uses
    Gemini as the reliable explanation path.
    """
    return (client or GeminiClient()).generate(explain_prompt(topic))
