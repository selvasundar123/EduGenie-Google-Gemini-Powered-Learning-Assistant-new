from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    AnswerResponse,
    HealthResponse,
    LearningPathRequest,
    QuestionRequest,
    QuizResponse,
    TextRequest,
    TextResponse,
)
from tests.services.gemini_client import (
    GeminiGenerationError,
    GeminiNotConfiguredError,
    gemini_is_configured,
    get_settings,
)
from summary_module import summarize_text

ROOT = Path(__file__).parent
FRONTEND_DIST = ROOT / "frontend" / "dist"
ROUTE_MANIFEST = ROOT / "manus-routes.json"

app = FastAPI(
    title="EduGenie API",
    description="A Gemini-powered learning assistant for questions, explanations, quizzes, summaries, and learning paths.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


def model_error(exc: Exception) -> HTTPException:
    if isinstance(exc, GeminiNotConfiguredError):
        return HTTPException(status_code=503, detail=str(exc))
    if isinstance(exc, GeminiGenerationError):
        return HTTPException(status_code=502, detail=str(exc))
    return HTTPException(status_code=500, detail="EduGenie could not complete that request.")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        gemini_configured=gemini_is_configured(),
        demo_mode=settings["demo_mode"],
    )


@app.get("/manus-routes.json")
def routes_manifest() -> JSONResponse:
    if ROUTE_MANIFEST.exists():
        return JSONResponse(json.loads(ROUTE_MANIFEST.read_text()))
    return JSONResponse({"routes": [{"path": "/", "title": "EduGenie"}]})


@app.post("/qa", response_model=AnswerResponse)
def qa(request: QuestionRequest) -> AnswerResponse:
    try:
        return AnswerResponse(answer=answer_question(request.question))
    except Exception as exc:
        raise model_error(exc) from exc


@app.post("/explain", response_model=TextResponse)
def explain(request: TextRequest) -> TextResponse:
    try:
        return TextResponse(result=explain_concept(request.text))
    except Exception as exc:
        raise model_error(exc) from exc


@app.post("/quiz", response_model=QuizResponse)
def quiz(request: TextRequest) -> QuizResponse:
    try:
        return QuizResponse(questions=generate_quiz(request.text))
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise model_error(exc) from exc


@app.post("/summarize", response_model=TextResponse)
def summarize(request: TextRequest) -> TextResponse:
    try:
        return TextResponse(result=summarize_text(request.text))
    except Exception as exc:
        raise model_error(exc) from exc


@app.post("/learn/recommendations", response_model=TextResponse)
def learn_recommendations(request: LearningPathRequest) -> TextResponse:
    try:
        return TextResponse(result=get_learning_recommendations(request.topic, request.level))
    except Exception as exc:
        raise model_error(exc) from exc


@app.get("/", include_in_schema=False, response_model=None)
def index() -> FileResponse | JSONResponse:
    index_file = FRONTEND_DIST / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(
        {
            "name": "EduGenie",
            "message": "Frontend not built. Run `cd frontend && npm install && npm run build`.",
            "docs": "/docs",
        }
    )
