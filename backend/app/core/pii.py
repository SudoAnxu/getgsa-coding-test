import re

EMAIL_RE = re.compile(r"""\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b""")
PHONE_RE = re.compile(r"""(?:(?:(?:\+?1\s*[-.]?\s*)?\(?\d{3}\)?|\d{3})\s*[-.]?\s*\d{3}\s*[-.]?\s*\d{4})""")

def redact(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text
