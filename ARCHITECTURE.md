# Architecture

```
+-------------+        +-------------------+         +-------------------+
|  UI (Web)   | <----> |  API (FastAPI)    | <-----> |  Storage (Memory) |
| Streamlit   |        | /ingest, /analyze |         |  (per-request)    |
+-------------+        +---------+---------+         +---------+---------+
                                  |                             |
                                  v                             v
                           +------+-------+               +-----+-------+
                           |  Core Logic  |               |  RAG Index  |
                           |  redact/extract/classify     |  R1..R5      |
                           |  checklist+brief/email       |  naive retr. |
                           +--------------+---------------+--------------+
```

- **PII Redaction**: regex masks emails and phones before storage.
- **Extraction**: simple regex + parsing for UEI, DUNS, NAICS, SAM status, PP fields, pricing rows.
- **Classification**: rule-based + mock LLM (abstains when low confidence).
- **RAG**: tiny in-memory index with keyword tagging and cosine-like token overlap retrieval.
- **Scalability**: API is stateless; request state keyed by `request_id`. Swap memory with Redis/S3/DB. Add queues (e.g., Celery) for batch analysis.
- **Extensibility**: new "Pricing Pack v2" → add `rules_pack_v2.py` and register in vectorstore without breaking older IDs.
