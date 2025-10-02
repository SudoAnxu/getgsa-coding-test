# GetGSA — AI + RAG mini-slice

This is a minimal, **working** slice that matches the assignment spec:
- Ingest docs (redact PII) → `/ingest`
- Analyze (classify, extract fields, build RAG checklist, generate brief + client email) → `/analyze`
- Health check → `/healthz`
- Single-page UI (Streamlit) with *Ingest* and *Analyze* buttons
- Tiny **RAG** over R1–R5 with citations
- **Abstention** paths for uncertain classification
- **Tests** and a `make test` runner

## Quick start

```bash
# 1) Create and activate venv (recommended)
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2) Install
make install

# 3) Run API (dev)
make run

# 4) Open API docs
# http://127.0.0.1:8000/docs

# 5) Run the Streamlit UI (in another terminal)
make ui

# 6) Run tests
make test
```

## Project layout
See `ARCHITECTURE.md` for the component flow. Prompts are in `PROMPTS.md`, security notes in `SECURITY.md`.
