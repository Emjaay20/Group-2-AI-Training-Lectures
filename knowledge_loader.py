from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"
KNOWLEDGE = ROOT / "knowledge"

LABS = [
    ("all", "Course map (all labs)", ["course_map.md"]),
    ("collect", "1 · Data collection", ["course_map.md", "01_data_collection.md"]),
    ("hf", "2 · Hugging Face three ways", ["course_map.md", "02_huggingface.md"]),
    ("sentiment", "3 · Headline sentiment", ["course_map.md", "03_sentiment.md"]),
    ("vision", "4 · OpenCV & YOLO", ["course_map.md", "04_opencv_yolo.md"]),
    ("privacy", "5 · Screen privacy", ["course_map.md", "05_screen_privacy.md"]),
    ("anpr", "6 · ANPR gate", ["course_map.md", "06_anpr.md"]),
    ("ideas", "7 · Lab ideas (conceptual)", ["course_map.md", "07_lab_ideas.md"]),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def system_prompt() -> str:
    return read_text(PROMPTS / "system.md")


def lab_context(lab_key: str) -> str:
    files = next((files for key, _label, files in LABS if key == lab_key), ["course_map.md"])
    parts = []
    for name in files:
        path = KNOWLEDGE / name
        if path.exists():
            parts.append(read_text(path))
    return "\n\n".join(parts)


def build_messages(lab_key: str, history: list[dict]) -> list[dict]:
    sys = system_prompt()
    notes = lab_context(lab_key)
    combined = (
        sys
        + "\n\n---\n# Active lab notes (ground your answer here)\n\n"
        + notes
    )
    return [{"role": "system", "content": combined}, *history]
