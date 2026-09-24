# NDC Class 2026 AI course map

Official labs live in https://github.com/emmanuelsheshi/NDC_class2026

Typical flow the class actually ran:

1. Collect messy web text (Playwright → JSON headlines).
2. Run NLP two ways: Hugging Face `pipeline` (easy) and raw tokenizer + model (what the pipeline hides).
3. Call a hosted instruct model over an OpenAI-compatible API (HF router / Groq-style) to label sentiment in bulk.
4. Move from language to vision: OpenCV camera, then YOLO detect and segment.
5. Two applied systems:
   - Screen privacy / shoulder-surfing monitor (pose + gaze heuristic).
   - Vehicle gate ANPR (detect → crop plate → OCR → allow-list).

Dependencies used in class (`requirements.txt`): playwright, openai, transformers, torch, requests, ultralytics, opencv-python. ANPR also needs EasyOCR in practice.

Mental model to teach: **collect → structure → infer → act**.
Text labs collect and classify. Vision labs perceive and trigger a policy (blur screen, grant/deny gate).
