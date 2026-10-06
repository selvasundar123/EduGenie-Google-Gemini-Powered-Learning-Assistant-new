from tests.services.gemini_client import GeminiClient
from tests.services.prompts import learning_path_prompt


def get_learning_recommendations(
    topic: str, level: str = "beginner", client: GeminiClient | None = None
) -> str:
    return (client or GeminiClient()).generate(learning_path_prompt(topic, level))
