from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Please enter some text before submitting.")
        return value


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=8_000)

    @field_validator("question")
    @classmethod
    def clean_question(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Please enter a question before submitting.")
        return value


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=2_000)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Please enter a topic before requesting a learning path.")
        return value


class AnswerResponse(BaseModel):
    answer: str


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_index: int = Field(ge=0, le=3)
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    demo_mode: bool
