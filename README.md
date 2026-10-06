# EduGenie

EduGenie is a Gemini-powered learning assistant for students and self-learners. It turns questions, dense passages, and study topics into clearer explanations, quick quizzes, summaries, and personalized learning paths.

## What is included

The FastAPI backend exposes five endpoints: `POST /qa`, `POST /explain`, `POST /quiz`, `POST /summarize`, and `POST /learn/recommendations`. The React frontend provides a responsive learning workspace for all five tools. Gemini is called only from the server, so the browser never sees the API key. Quiz responses are validated and normalized into exactly three questions with four options each. The concept explanation module is intentionally structured so an optional LaMini-Flan-T5 local adapter can be added later; the default path is Gemini because it keeps the first setup lightweight.

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- A Google AI Studio Gemini API key for live responses

## Quick start

```bash
# from the project root
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set GEMINI_API_KEY

cd frontend
npm install
npm run dev                       # React UI at http://127.0.0.1:5173
```

In a second terminal, run the API:

```bash
cd EduGenie
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

The FastAPI docs are available at `http://127.0.0.1:8000/docs`. The Vite dev server proxies the five API routes to FastAPI.

## Single-server preview / production-style run

Build the React app into `frontend/dist`, then let FastAPI serve the compiled frontend:

```bash
cd frontend
npm run build
cd ..
uvicorn main:app --host 0.0.0.0 --port 3000
```

Open `http://127.0.0.1:3000`. The health check is `GET /health`, and the Web Dev route manifest is `GET /manus-routes.json`.

## Environment variables

| Variable | Purpose | Example |
| --- | --- | --- |
| `GEMINI_API_KEY` | Google AI Studio key used server-side | `your-key-here` |
| `GEMINI_MODEL` | Model name to call | `gemini-2.0-flash` |
| `DEMO_MODE` | Enables empty demo responses only when no key is present; keep false for real learning output | `false` |

Never commit `.env` or expose `GEMINI_API_KEY` in React code.

## API examples

```bash
curl -X POST http://127.0.0.1:8000/qa \\
  -H 'Content-Type: application/json' \\
  -d '{"question":"Which is the largest ocean?"}'

curl -X POST http://127.0.0.1:8000/quiz \\
  -H 'Content-Type: application/json' \\
  -d '{"text":"The water cycle describes evaporation, condensation, and precipitation."}'

curl -X POST http://127.0.0.1:8000/learn/recommendations \\
  -H 'Content-Type: application/json' \\
  -d '{"topic":"SQL for data analysis","level":"beginner"}'
```

## Project structure

```text
EduGenie/
├── main.py                       # FastAPI app and REST endpoints
├── schemas.py                    # Pydantic request/response contracts
├── qna.py                        # Q&A use case
├── explanation_module.py         # Concept explanations and local-model seam
├── quiz_module.py                # Quiz generation and validation
├── summary_module.py             # Passage summarization
├── learning_path.py              # Personalized learning paths
├── tests.services/
│   ├── gemini_client.py          # Server-side Gemini SDK wrapper
│   ├── parsers.py                # JSON fence cleanup and quiz normalization
│   └── prompts.py                # Prompt templates
├── frontend/
│   ├── src/App.jsx               # React workspace and result renderers
│   ├── src/styles.css            # Responsive visual system
│   └── public/edugenie-mark.svg  # Project-specific logo and favicon
├── tests/                        # API contract and parsing tests
├── requirements.txt
├── .env.example
└── manus-routes.json
```

## Testing

```bash
source .venv/bin/activate
pytest -q
python3 -m compileall main.py schemas.py qna.py explanation_module.py quiz_module.py summary_module.py learning_path.py tests.services
```

The tests do not call Gemini. They validate input contracts, endpoint wiring, and structured quiz parsing with mocked responses.
