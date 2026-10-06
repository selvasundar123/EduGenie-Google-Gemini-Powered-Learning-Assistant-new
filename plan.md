# EduGenie implementation plan

## Product outcome

EduGenie is a small learning workspace with five Gemini-powered actions: question answering, concept explanation, quiz generation, passage summarization, and personalized learning recommendations.

## Architecture

The application uses a FastAPI server as the single runtime boundary. The React/Vite frontend is developed independently and compiled into `frontend/dist`; FastAPI serves that compiled output for a single-server run. During local development, Vite proxies API requests to Uvicorn. The Gemini API key remains server-side in environment variables. No user account, database, payment, or scheduled job is required for this first version.

## API and data contracts

Pydantic models validate all input. The `/quiz` endpoint additionally normalizes Gemini JSON into three questions with four options and a zero-based `correct_index`. Model and configuration failures map to readable 503/502 errors, while `/health` remains available without a key. The route manifest is served at `/manus-routes.json`.

## Verification

Use `pytest -q` for contract and parser tests, `python3 -m compileall` for Python syntax, `npm run build` for the React production bundle, then start Uvicorn on the configured preview port and verify `/health`, `/manus-routes.json`, and `/` with HTTP requests. Gemini calls are mocked in tests and require a user-provided key only for live learning requests.
