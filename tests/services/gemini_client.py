from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class GeminiNotConfiguredError(RuntimeError):
    """Raised when the app needs a Gemini key but none is configured."""


class GeminiGenerationError(RuntimeError):
    """Raised when Gemini cannot produce a response."""


@lru_cache(maxsize=1)
def get_settings() -> dict[str, Any]:
    return {
        "api_key": os.getenv("GEMINI_API_KEY", "").strip(),
        "model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip(),
        "demo_mode": os.getenv("DEMO_MODE", "false").lower() in {"1", "true", "yes"},
    }


def gemini_is_configured() -> bool:
    return bool(get_settings()["api_key"])


class GeminiClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings["api_key"]
        self.model = settings["model"]
        self.demo_mode = settings["demo_mode"]
        self._client = None

    def _get_client(self):
        if self.demo_mode and not self.api_key:
            return None
        if not self.api_key:
            raise GeminiNotConfiguredError(
                "Gemini is not configured. Add GEMINI_API_KEY to your .env file."
            )
        if self._client is None:
            try:
                from google import genai

                self._client = genai.Client(api_key=self.api_key)
            except Exception as exc:  # pragma: no cover - dependency/runtime specific
                raise GeminiGenerationError(f"Could not initialize Gemini: {exc}") from exc
        return self._client

    def generate(self, prompt: str, *, json_mode: bool = False) -> str:
        client = self._get_client()
        if client is None:
            return ""
        try:
            from google.genai import types

            config = types.GenerateContentConfig(
                temperature=0.35,
                response_mime_type="application/json" if json_mode else "text/plain",
            )
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            text = getattr(response, "text", None)
            if not text:
                raise GeminiGenerationError("Gemini returned an empty response.")
            return text.strip()
        except GeminiGenerationError:
            raise
        except Exception as exc:  # pragma: no cover - network/provider specific
            raise GeminiGenerationError(f"Gemini request failed: {exc}") from exc
