
# GetGSA — Coding Test Solution

This project implements a minimal working slice of **GetGSA (AI + RAG)** as per the coding test requirements.

---

## ✨ Features Implemented
- **Document ingestion** (`POST /ingest`)
  - Accepts raw text docs, optional type hints.
  - Redacts PII (emails & phone numbers) before storing.
- **Analysis pipeline** (`POST /analyze`)
  - Document classification (profile / past performance / pricing / unknown) with abstention.
  - Field extraction (UEI, DUNS, NAICS, SAM status, PP details, pricing rows).
  - **RAG checklist** against rules **R1–R5** with citations.
  - Negotiation **Prep Brief** (2–3 paragraphs).
  - Polite **Client Email Draft** summarizing gaps.
- **UI (Streamlit)**: simple 2-pane interface to ingest and analyze docs.
- **Tests** (Pytest):
  - Missing UEI → `missing_uei` flagged (R1).
  - Past performance < $25k → `past_performance_min_value_not_met` (R3).
  - NAICS→SIN mapping with dedupe (R2).
  - PII redaction masks emails/phones (R5).
  - RAG sanity test when R1 removed.
- **Docs provided**:
  - `ARCHITECTURE.md` → flow & scalability notes.
  - `PROMPTS.md` → LLM prompts & abstention strategy.
  - `SECURITY.md` → redaction & abuse limits.

---

## 📂 Project Structure
```

backend/         # FastAPI app
│  ├─ app/
│  │  ├─ api/         # routes (ingest, analyze, healthz)
│  │  ├─ core/        # classification, extraction, rag, utils, pii
│  │  └─ main.py      # FastAPI entrypoint
data/samples/    # Sample input docs
tests/           # Pytest unit tests
ui/              # Streamlit single-page UI
docker/          # Dockerfile + docker-compose
ARCHITECTURE.md  # diagrams and scaling
PROMPTS.md       # LLM prompts
SECURITY.md      # security notes
README.md        # (this file)

````

---

## 🚀 Quick Start

### 1. Setup
```bash
# Create virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -U pip
pip install -r backend/requirements.txt
````

### 2. Run Backend (FastAPI)

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Frontend (Streamlit UI)

```bash
streamlit run ui/streamlit_app.py --server.port 8501
```

Open UI: [http://localhost:8501](http://localhost:8501)

### 4. Run Tests

```bash
pytest -q
```

---

## 🧪 How to Use

1. Open the UI → select a sample doc (e.g., Company Profile A) → **Ingest**.
2. Copy the `request_id` returned.
3. Paste it into the right pane and click **Analyze**.
4. You’ll see parsed fields, checklist (with R# citations), prep brief, client email, and citations.

---

## 🐳 Run with Docker (Optional)

```bash
docker build -t getgsa .
docker run -p 8000:8000 getgsa
```

---

## 📌 Notes

* **Abstention**: Classifier or checklist returns `"unknown"` / `"needs_human"` when low confidence or missing rules.
* **Extensibility**: Adding *Pricing Pack v2* → extend `rules_pack.py` and re-index without breaking old logic.
* **Scalability**: Stateless API, request state keyed by `request_id`. Replace in-memory store with Redis/DB for production.

---

👨‍💻 Author: *[Priyangshu Karmakar]*



👉 Do you want me to also **add a sample run section** (with screenshots of UI + API JSON response) so it looks extra convincing when they open the repo/zip?
```
