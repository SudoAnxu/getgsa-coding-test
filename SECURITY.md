# Security Notes

- **Redaction**: All emails and US phone numbers are masked at ingest (`[REDACTED_EMAIL]`, `[REDACTED_PHONE]`). Only derived fields are stored alongside redacted text.
- **Max Input Size**: 200k chars per request (basic guard to prevent abuse).
- **Abuse Limits**: Reject >50 docs per ingest, and rate-limit `/analyze` per request_id in production.
- **SSRF/XSS**: No external fetches; UI posts raw text; API returns JSON only.
- **Prompt Injection**: RAG limits to rules R1–R5 and uses citations. Model must abstain when unsure.
