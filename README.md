---
title: NDC Class 2026 AI Tutor
emoji: 🛡️
colorFrom: green
colorTo: yellow
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
short_description: Course tutor for the NDC Class 2026 AI labs
---

# NDC Class 2026 AI Course Tutor

Custom chatbot + GUI for the labs in
[emmanuelsheshi/NDC_class2026](https://github.com/emmanuelsheshi/NDC_class2026).

It explains what the class actually built: Playwright headline collection,
Hugging Face (router / pipeline / direct model), sentiment JSON, OpenCV + YOLO,
the screen-privacy pose demo, and the ANPR gate.

Two engines, one app:

| Mode | Where | Model |
|---|---|---|
| Office laptop | LM Studio at `http://127.0.0.1:1234/v1` | `gemma-4-e4b` |
| Public Hugging Face Space | Groq OpenAI-compatible API | `llama-3.1-8b-instant` (or `llama-3.3-70b-versatile`) |

## 1. Run locally (Gemma 4 E4B)

1. Open **LM Studio**.
2. Load **Google Gemma 4 E4B**.
3. Developer tab → start the local server on port **1234**.
4. Confirm:

```bash
curl http://127.0.0.1:1234/v1/models
```

5. In this folder:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

6. In the sidebar leave **Local · LM Studio · Gemma 4 E4B** selected.
   If `/v1/models` shows a longer id (`google/gemma-4-e4b`, a QAT name, etc.),
   paste that exact string into **Model id**.

## 2. Put it online (Hugging Face Space + Groq)

1. Create a free key at [console.groq.com](https://console.groq.com).
2. Create a new **Streamlit** Space and push this folder
   (`app.py` must stay at the repo root of the Space).
3. Space → Settings → **Secrets**:

```
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.1-8b-instant
```

4. The app detects `SPACE_ID` and defaults the sidebar to Groq.
   Class laptops can still switch back to Local when they clone the same code.

Do not put classified or personal operational text into the public Space.

## What the GUI is doing

- **System prompt** (`prompts/system.md`) — NDC lab instructor, mixed tone,
  dry jokes only when the question is playful or slightly off-syllabus,
  then a steer back to a lab.
- **Lab focus** — injects the matching notes from `knowledge/` so a 4B local
  model is not guessing the syllabus.
- **Chat** — OpenAI-style messages streamed into Streamlit.
- **Check connection** — hits `/v1/models` on whichever backend is selected.

## Team split

- One person: confirm LM Studio model id on a class laptop.
- One person: Groq key + Hugging Face Space secrets.
- One person: read `prompts/system.md` and tighten voice if the Commandant
  wants a stricter briefing tone.
- Whole room: ask each starter question in the sidebar and file wrong answers
  as prompt / knowledge-pack edits — not as “the model is broken.”

## Safety

The tutor may discuss the *idea* that NLP can structure open news text.
It must not teach dark-web access, exploits, weapons, or covert surveillance.
The privacy and ANPR labs are classroom demos (lock disabled by default;
allow-list includes `NDC2026`).
