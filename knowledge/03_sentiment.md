# Lab: Headline sentiment analysis

File: `3_analysis.py`. Inputs: `headlines.json`. Output: `sentiment_results.json`.

## Purpose
Batch-label collected news titles with an instruct model and keep a structured audit file.

## Flow
1. Load headlines from JSON (fail clearly if the scrape file is missing — collection must run first).
2. Authenticate to a Hugging Face / OpenAI-compatible inference endpoint.
3. Prompt a large instruct model (class script used a Llama-3.3-70B-Instruct style model) with low temperature (~0.1).
4. Ask for a JSON array. Each item: headline, sentiment (`POSITIVE` | `NEGATIVE` | `NEUTRAL`), confidence, short reason.
5. Strip markdown fences if the model wraps the JSON in ``` blocks.
6. Save `sentiment_results.json`.

## Teaching points
- Sentiment on crime headlines will skew negative. That is expected. The value is consistent labels + reasons, not cheerfulness.
- Low temperature = more repeatable labels for a class demo.
- Always sanitise model output before `json.loads`.
- This is the “act on collected text” step after Playwright.

## Operational analogy (keep it conceptual)
A watch floor can turn a river of open headlines into a short tagged list: what looks alarming, what is routine, why the model said so. A human still decides. The lab is not an automatic targeting system.
