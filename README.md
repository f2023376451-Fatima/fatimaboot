# FatimaBot — Personal RAG Chatbot

**FatimaBot** is a Retrieval-Augmented Generation (RAG) chatbot for **Ghulam Fatima**, a BS Artificial Intelligence student at UMT Lahore and AI Intern at Ascend Analytics.

It answers questions about her education, internship, skills, projects, and contact details using her own curated knowledge base.

---

## RAG Architecture (matches the required diagram)

```
1. Additional documents (JSONL knowledge chunks)
       ↓ Encode
2. Embedding model (all-MiniLM-L6-v2)
       ↓ Index
3. Vector database (FAISS)

4. User Query → Encode → Similarity search → Similar documents
       ↓
5. Prompt = Query + Retrieved documents
       ↓
6. LLM (Gemini / DeepSeek / OpenAI-compatible)
       ↓
7. Final response
```

**Also included:** conversation history, optional source transparency, retrieval-only fallback (works without API key).

---

## Tech Stack

| Component     | Choice                                      |
|---------------|---------------------------------------------|
| Embeddings    | `all-MiniLM-L6-v2` (sentence-transformers)  |
| Vector store  | FAISS (`IndexFlatIP`, cosine)               |
| LLM           | Gemini 2.0 Flash (default) / OpenAI-compatible |
| Interface     | Streamlit (+ optional CLI)                  |
| Knowledge     | 41 personal chunks (JSONL)                  |

---

## Folder Structure

```
fatimabot/
├── app.py                          # Streamlit UI (main entry)
├── rag_engine.py                   # Full RAG pipeline
├── cli_chat.py                     # Optional terminal chat
├── ghulam_fatima_knowledge.jsonl   # Knowledge base (REQUIRED)
├── ghulam_fatima_qa_dataset.json   # Source Q&A pairs
├── requirements.txt
├── README.md
└── .streamlit/config.toml
```

---

## Dataset

**File:** `ghulam_fatima_knowledge.jsonl` (included)

Built from Ghulam Fatima’s personal CV. Covers:

- Full name, contact (phone, email), Lahore
- Education: BS Artificial Intelligence @ UMT Lahore (2023–2027), 7th semester, CGPA 3.27/4.0
- Internship: AI Intern @ Ascend Analytics (2026–Present) — LangChain, LLMs, Python
- Projects: LangChain AI Application (Tavily), Pakistan Environmental Data Engineering (PostgreSQL), ML classification/prediction
- Skills: Python, LangChain, LLM Applications, Machine Learning, PostgreSQL, MySQL, SQLite, SQL, HTML, CSS
- Tools: VS Code, Google Colab, Jupyter, Excel, Word, PowerPoint
- Soft skills, languages (Urdu Native / English Professional)
- Core subjects: ML, Deep Learning, DBMS, OS, Data Visualization

Data is preprocessed and indexed with FAISS for retrieval.

---

## Setup & Run

```bash
cd fatimabot
pip install -r requirements.txt
streamlit run app.py
```

Optional API key for natural answers:

```bash
export GEMINI_API_KEY=your-key-here
# or DEEPSEEK_API_KEY / OPENAI_API_KEY
```

Without a key the bot still works in **retrieval-only** mode.

**CLI test:**
```bash
python cli_chat.py
```

---

## Deployment (Streamlit Cloud)

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `app.py`
4. (Optional) Secrets:

```toml
GEMINI_API_KEY = "your-key-here"
```

---

## Features

- Named identity: **FatimaBot**
- Full RAG pipeline (load → embed → index → retrieve → prompt → generate)
- Conversation history
- Optional “Show retrieved sources”
- Works with or without LLM API key
- Supports Gemini, DeepSeek, and OpenAI-compatible endpoints
- Clean Streamlit UI

---

## How the code maps to the RAG diagram

| Diagram step              | Code location                          |
|---------------------------|----------------------------------------|
| 1. Additional documents   | `ghulam_fatima_knowledge.jsonl` + `load_documents()` |
| 2. Encode (embedding)     | `build_embeddings()` — sentence-transformers |
| 3. Index → Vector DB      | `build_index()` — FAISS IndexFlatIP    |
| 4. Query encode + search  | `retrieve()` — similarity search       |
| 5. Similar documents      | top-k results with scores              |
| 6. Prompt + Query         | `build_prompt()`                       |
| 7. LLM → Final response   | `generate()` — OpenAI-compatible client |

---

## Contact (subject of the bot)

**Ghulam Fatima**  
BS Artificial Intelligence · UMT Lahore (7th semester, CGPA 3.27)  
AI Intern · Ascend Analytics  
Email: gf3786755@gmail.com  
Phone: 03039936041  
Lahore, Pakistan
