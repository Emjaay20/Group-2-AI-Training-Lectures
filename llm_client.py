"""OpenAI-compatible client for LM Studio (local Gemma) and Groq (cloud)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI

LMSTUDIO_BASE = os.environ.get("LMSTUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
GROQ_BASE = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
DEFAULT_LOCAL_MODEL = os.environ.get("LOCAL_MODEL", "gemma-4-e4b")
DEFAULT_GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")


@dataclass
class Backend:
    key: str
    label: str
    base_url: str
    model: str
    api_key: str


def available_backends() -> dict[str, Backend]:
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    return {
        "local": Backend(
            key="local",
            label="Local · LM Studio · Gemma 4 E4B",
            base_url=LMSTUDIO_BASE,
            model=os.environ.get("LOCAL_MODEL", DEFAULT_LOCAL_MODEL),
            api_key=os.environ.get("LMSTUDIO_API_KEY", "lm-studio"),
        ),
        "groq": Backend(
            key="groq",
            label="Cloud · Groq",
            base_url=GROQ_BASE,
            model=os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL),
            api_key=groq_key or "missing-groq-key",
        ),
    }


def make_client(backend: Backend) -> OpenAI:
    return OpenAI(base_url=backend.base_url, api_key=backend.api_key)


def stream_chat(
    backend: Backend,
    messages: list[dict],
    temperature: float = 0.6,
    max_tokens: int = 4096,
):
    client = make_client(backend)
    return client.chat.completions.create(
        model=backend.model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )


def ping_backend(backend: Backend) -> tuple[bool, str]:
    """Best-effort check so the GUI can show a live/dead badge."""
    try:
        client = make_client(backend)
        models = client.models.list()
        ids = [m.id for m in models.data][:8]
        if not ids:
            return True, "Server reached (no model ids listed)."
        return True, ", ".join(ids)
    except Exception as exc:  # noqa: BLE001 — surface any transport error in the UI
        return False, str(exc)
