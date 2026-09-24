"""NDC Class 2026 AI Course Tutor — Streamlit GUI."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from knowledge_loader import LABS, build_messages
from llm_client import available_backends, ping_backend, stream_chat

load_dotenv()

st.set_page_config(
    page_title="NDC Class 2026 AI Tutor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

STARTERS = {
    "all": [
        "Give the class a 2-minute briefing of everything we covered.",
        "What is the collect → structure → infer → act pattern?",
        "Which lab should a complete beginner revisit first?",
    ],
    "collect": [
        "Why did we use Playwright instead of requests?",
        "What fields end up in the headlines JSON?",
        "How does this scrape feed the sentiment lab?",
    ],
    "hf": [
        "Explain pipeline vs direct tokenizer+model like I am new.",
        "How is the Hugging Face router similar to LM Studio?",
        "What does GPT-2 generation hide from us?",
    ],
    "sentiment": [
        "Walk through 3_analysis.py step by step.",
        "Why use temperature 0.1 for labels?",
        "What should we do if the model wraps JSON in markdown?",
    ],
    "vision": [
        "Detect vs segment vs pose — one sentence each.",
        "Why do IP cameras break in OpenCV?",
        "What does the nano YOLO weight buy us?",
    ],
    "privacy": [
        "How does the lab decide who the Primary Operator is?",
        "Why is the real workstation lock off by default?",
        "Is the gaze check real eye tracking?",
    ],
    "anpr": [
        "Draw the ANPR pipeline from camera to GRANTED/DENIED.",
        "Why run EasyOCR only every 10 frames?",
        "What does the demo key 'a' do?",
    ],
    "ideas": [
        "What transferable skill is LabIdeas.txt actually pointing at?",
        "Keep it conceptual: how does headline NLP resemble a watch-floor brief?",
    ],
}


def inject_css() -> None:
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
          
          /* Modern Typography */
          html, body, [class*="css"] { 
            font-family: "Outfit", sans-serif; 
          }
          
          .block-container { 
            padding-top: 1.2rem; 
            max-width: 1100px; 
          }
          
          /* Glassmorphic Hero Banner */
          .ndc-hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.9) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            color: #f8fafc;
            padding: 1.5rem 1.8rem;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
          }
          .ndc-hero:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
          }
          .ndc-hero h1 {
            font-weight: 700;
            font-size: 1.9rem;
            margin: 0 0 0.4rem 0;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
          }
          .ndc-hero p { margin: 0; opacity: 0.85; font-size: 1rem; line-height: 1.5; }
          
          /* Chat Message Styling & Animation */
          @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
          }
          .stChatMessage {
            border-radius: 14px;
            animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            padding: 1rem;
            margin-bottom: 0.5rem;
          }
          
          /* Button Hover Effects */
          .stButton > button {
            border-radius: 12px;
            transition: all 0.2s ease;
            font-weight: 500;
          }
          .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
          }
          
          /* Custom Scrollbar */
          ::-webkit-scrollbar { width: 8px; height: 8px; }
          ::-webkit-scrollbar-track { background: transparent; }
          ::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.5); border-radius: 10px; }
          ::-webkit-scrollbar-thumb:hover { background: rgba(156, 163, 175, 0.8); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "backend_key" not in st.session_state:
        # Prefer local on a class laptop; HF Spaces will not have LM Studio.
        running_on_spaces = bool(os.environ.get("SPACE_ID") or os.environ.get("SPACE_HOST"))
        st.session_state.backend_key = "groq" if running_on_spaces else "local"


def render_hero() -> None:
    st.markdown(
        """
        <div class="ndc-hero">
          <h1>NDC Class 2026 · AI Course Tutor</h1>
          <p>Explains the labs in <b>emmanuelsheshi/NDC_class2026</b> — collection, Hugging Face, sentiment, OpenCV/YOLO, screen privacy, and the ANPR gate. Local Gemma via LM Studio, or Groq in the cloud.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar(backends) -> tuple:
    with st.sidebar:
        st.markdown("### Lab Focus")
        lab_key = st.selectbox(
            "Ground answers in specific course material:",
            options=[k for k, _l, _f in LABS],
            format_func=lambda k: next(l for key, l, _ in LABS if key == k),
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("⚙️ Advanced Settings"):
            labels = {k: b.label for k, b in backends.items()}
            backend_key = st.radio(
                "Engine",
                options=list(backends.keys()),
                format_func=lambda k: labels[k],
                index=list(backends.keys()).index(st.session_state.backend_key)
                if st.session_state.backend_key in backends
                else 0,
            )
            st.session_state.backend_key = backend_key
            backend = backends[backend_key]

            model_override = st.text_input(
                "Model id",
                value=backend.model,
                help="Override the default model ID.",
            )
            backend.model = model_override.strip() or backend.model

            if st.button("Check connection", use_container_width=True):
                with st.spinner("Checking..."):
                    ok, detail = ping_backend(backend)
                if ok:
                    st.success(f"Reachable. Models: {detail}")
                else:
                    st.error(detail)
                    
            temperature = st.slider("Temperature", 0.0, 1.2, 0.55, 0.05)
            
            if backend_key == "local":
                st.caption("Local: Start LM Studio server on port 1234.")
            else:
                if not os.environ.get("GROQ_API_KEY"):
                    st.warning("Set GROQ_API_KEY in .env")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.toast("Chat cleared!", icon="🧹")
            st.rerun()

        st.markdown("---")
        st.caption("Repo: github.com/emmanuelsheshi/NDC_class2026")
        return backend, lab_key, temperature


def main() -> None:
    inject_css()
    init_state()
    render_hero()
    backends = available_backends()
    backend, lab_key, temperature = sidebar(backends)

    # Empty State for Starter Questions
    if not st.session_state.messages:
        st.markdown("<h3 style='text-align: center; margin-top: 2rem; color: #94a3b8;'>Try asking...</h3>", unsafe_allow_html=True)
        cols = st.columns(len(STARTERS.get(lab_key, STARTERS["all"])))
        for idx, q in enumerate(STARTERS.get(lab_key, STARTERS["all"])):
            with cols[idx]:
                if st.button(q, key=f"ask-{q[:40]}", use_container_width=True):
                    st.session_state.pending = q
        st.markdown("<br>", unsafe_allow_html=True)

    # Main Chat Loop
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pending = st.session_state.pop("pending", None)
    user_text = st.chat_input("Ask about a lab, a file, or why we built it that way…")
    prompt = pending or user_text

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        history = [
            m for m in st.session_state.messages if m["role"] in ("user", "assistant")
        ]
        # Keep last 8 turns so Gemma 4B does not drown.
        clipped = history[-16:]
        messages = build_messages(lab_key, clipped)

        with st.chat_message("assistant"):
            box = st.empty()
            acc = ""
            try:
                stream = stream_chat(backend, messages, temperature=temperature)
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    acc += delta
                    box.markdown(acc + "▌")
                box.markdown(acc or "_Empty reply — check the model id and that a model is loaded._")
            except Exception as exc:  # noqa: BLE001
                acc = (
                    "**Could not reach the model.**\n\n"
                    f"`{exc}`\n\n"
                    "Local: start LM Studio server on port 1234 and load Gemma 4 E4B. "
                    "Cloud: set `GROQ_API_KEY` and use a current Groq model id."
                )
                box.markdown(acc)
        st.session_state.messages.append({"role": "assistant", "content": acc})


if __name__ == "__main__":
    main()
