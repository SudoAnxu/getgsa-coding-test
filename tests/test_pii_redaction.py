from backend.app.core.pii import redact

def test_pii_redaction():
    text = "Contact me at john@abc.com or (415) 555-0100."
    red = redact(text)
    assert "[REDACTED_EMAIL]" in red
    assert "[REDACTED_PHONE]" in red
