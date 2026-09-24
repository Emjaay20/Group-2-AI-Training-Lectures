# Lab: Hugging Face three ways

Files: `2_A_hugginFace_interface.py`, `2_B_pipeline.py`, `2_C_direct_method.py`.

The point of Day 2 is not “pick one library.” It is to see **the same idea at three altitudes**.

## 2_A — OpenAI-compatible hosted client
- `OpenAI` client with `base_url="https://router.huggingface.co/v1"`.
- Chat completions against a routed model (class file used a Groq-hosted model id through that router).
- System + user messages. This is the same pattern this tutor uses with LM Studio and Groq.

Teaching point: if a server speaks the OpenAI chat schema, your Python client can swap endpoints (HF router, Groq, LM Studio on `http://127.0.0.1:1234/v1`) with almost no code change.

## 2_B — `transformers.pipeline` (easy mode)
- `pipeline("sentiment-analysis")` on a short sentence.
- `pipeline("text-generation", model="gpt2")` with a robotics-style prompt, max_length ~30.

Teaching point: pipeline hides tokenizer, padding, device, decoding. Good for labs and prototypes.

## 2_C — Direct method (what pipeline hides)
- Load GPT-2 tokenizer + model.
- Tokenize prompt `"The future of embedded robotics relies on"`.
- `generate` a small number of new tokens.
- Decode back to text.

Teaching point: text in → token ids → model → token ids → text out. Officers who understand this are not stuck when a pipeline wrapper breaks.

## How to explain the stack
Hosted chat API (2_A) = easiest product path.
Pipeline (2_B) = local/small-task path.
Direct (2_C) = you own the knobs (max tokens, sampling).
