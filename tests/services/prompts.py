def qa_prompt(question: str) -> str:
    return f"""You are EduGenie, a precise and encouraging educational tutor. Answer the question below in 2-5 concise paragraphs. Explain unfamiliar terms, state uncertainty when needed, and never invent sources.\n\nQuestion: {question}"""


def explain_prompt(topic: str) -> str:
    return f"""Explain the topic below to a curious beginner. Use plain language, one analogy, and a short example. Structure the response with a clear definition, how it works, and a quick check-for-understanding question. Keep it under 350 words.\n\nTopic: {topic}"""


def quiz_prompt(text: str) -> str:
    return f"""Create exactly three educational multiple-choice questions from the passage below. Return only valid JSON with this shape: {{\"questions\":[{{\"question\":\"...\",\"options\":[\"A\",\"B\",\"C\",\"D\"],\"correct_index\":0,\"explanation\":\"...\"}}]}}. Use zero-based correct_index values from 0 to 3. Make distractors plausible, avoid trick questions, and ensure every answer is supported by the passage.\n\nPassage or topic: {text}"""


def summary_prompt(text: str) -> str:
    return f"""Summarize the educational passage below for fast revision. Preserve the key ideas and relationships, remove repetition, and use a short title followed by 4-7 bullet points. Keep the language accessible.\n\nPassage: {text}"""


def learning_path_prompt(topic: str, level: str) -> str:
    return f"""Design a practical learning path for {topic} for a {level} learner. Start with prerequisites and move from beginner to advanced concepts. Include a suggested timeline, weekly milestones, practice ideas, and trustworthy resource types (books, documentation, courses, or videos). Use clear headings and make the plan achievable alongside school or work.\n\nTopic: {topic}\nLearner level: {level}"""
