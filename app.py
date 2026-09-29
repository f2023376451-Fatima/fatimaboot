"""
FatimaBot — Personal RAG Chatbot for Ghulam Fatima
Streamlit interface with conversation history and retrieval transparency.
"""

import os
import streamlit as st

st.set_page_config(
    page_title="FatimaBot | Ghulam Fatima",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main-header {
        text-align: center;
        padding: 0.6rem 0 0.2rem 0;
    }
    .main-header h1 {
        font-size: 1.85rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
        color: #0f172a;
    }
    .main-header p {
        color: #64748b;
        font-size: 0.95rem;
        margin: 0;
    }
    .stChatMessage {
        border-radius: 12px;
    }
    div[data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    .source-card {
        background: #f1f5f9;
        border-left: 3px solid #ec4899;
        padding: 0.55rem 0.75rem;
        margin: 0.35rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.82rem;
        color: #334155;
    }
    .footer-note {
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading FatimaBot knowledge base…")
def load_rag():
    from rag_engine import get_rag
    return get_rag()


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hey! I'm **FatimaBot** — personal assistant of Ghulam Fatima. "
                    "Ask me about her education, internship, skills, projects, or how to reach her."
                ),
            }
        ]
    if "show_sources" not in st.session_state:
        st.session_state.show_sources = False


def sidebar():
    with st.sidebar:
        st.markdown("### About FatimaBot")
        st.markdown(
            "Personal RAG chatbot built on Ghulam Fatima's knowledge base "
            "(profile, education, internship, skills, projects)."
        )
        st.markdown("---")
        st.markdown("**Ghulam Fatima**")
        st.caption("BS Artificial Intelligence · UMT Lahore")
        st.caption("7th Semester · CGPA 3.27/4.0")
        st.caption("AI Intern · Ascend Analytics")
        st.markdown("")
        st.markdown("📧 gf3786755@gmail.com")
        st.markdown("📱 03039936041")
        st.markdown("📍 Lahore, Pakistan")
        st.markdown("---")
        st.markdown("**Skills**")
        st.caption("Python · LangChain · LLMs · ML")
        st.caption("PostgreSQL · SQL · Data Engineering")
        st.markdown("---")

        api_key = st.text_input(
            "Gemini / DeepSeek / OpenAI API Key (optional)",
            type="password",
            help="Leave empty for retrieval-only mode. With a key, answers become more natural.",
            value=(
                os.getenv("GEMINI_API_KEY", "")
                or os.getenv("DEEPSEEK_API_KEY", "")
                or os.getenv("OPENAI_API_KEY", "")
            ),
        )
        base_url = st.selectbox(
            "LLM endpoint",
            options=[
                "https://generativelanguage.googleapis.com/v1beta/openai/",
                "https://api.deepseek.com",
                "https://api.openai.com/v1",
            ],
            index=0,
        )
        model_name = st.text_input("Model name", value="gemini-2.0-flash")

        st.session_state.show_sources = st.checkbox("Show retrieved sources", value=False)

        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. What would you like to know about Fatima?",
                }
            ]
            st.rerun()

        st.markdown("---")
        st.caption("RAG: Docs → Embed → FAISS → Retrieve → Prompt → LLM")
        return api_key, base_url, model_name


def main():
    init_session()
    api_key, base_url, model_name = sidebar()

    st.markdown(
        """
        <div class="main-header">
            <h1>🌸 FatimaBot</h1>
            <p>Personal AI assistant of Ghulam Fatima</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rag = load_rag()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources") and st.session_state.show_sources:
                with st.expander("Sources used"):
                    for s in msg["sources"]:
                        score = s.get("score", 0)
                        cat = s.get("category", "")
                        preview = s.get("text", "")[:160] + ("…" if len(s.get("text", "")) > 160 else "")
                        st.markdown(
                            f'<div class="source-card"><b>{cat}</b> · score {score:.2f}<br>{preview}</div>',
                            unsafe_allow_html=True,
                        )

    if prompt := st.chat_input("Ask about education, internship, skills, projects…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                history_for_rag = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                ]
                answer, retrieved = rag.generate(
                    query=prompt,
                    history=history_for_rag,
                    api_key=api_key if api_key else None,
                    base_url=base_url,
                    model=model_name,
                )
                st.markdown(answer)

                if st.session_state.show_sources and retrieved:
                    with st.expander("Sources used"):
                        for s in retrieved:
                            score = s.get("score", 0)
                            cat = s.get("category", "")
                            preview = s.get("text", "")[:160] + ("…" if len(s.get("text", "")) > 160 else "")
                            st.markdown(
                                f'<div class="source-card"><b>{cat}</b> · score {score:.2f}<br>{preview}</div>',
                                unsafe_allow_html=True,
                            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": retrieved if st.session_state.show_sources else None,
            }
        )

    st.markdown(
        '<p class="footer-note">Built with RAG · Embeddings: all-MiniLM-L6-v2 · Vector DB: FAISS</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
