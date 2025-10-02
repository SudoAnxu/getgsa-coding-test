import re
from typing import Dict, Any, List

UEI_RE = re.compile(r"""UEI:\s*([A-Za-z0-9]{12})""", re.I)
DUNS_RE = re.compile(r"""DUNS:\s*(\d{9})""", re.I)
NAICS_RE = re.compile(r"""NAICS:\s*([0-9,\s]+)""", re.I)
SAM_RE = re.compile(r"""SAM\.gov:\s*(registered|active|inactive|not\s+registered)""", re.I)

EMAIL_RE = re.compile(r"""\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b""")
PHONE_RE = re.compile(r"""(?:(?:(?:\+?1\s*[-.]?\s*)?\(?\d{3}\)?|\d{3})\s*[-.]?\s*\d{3}\s*[-.]?\s*\d{4})""")

VALUE_RE = re.compile(r"""Value:\s*\$?([0-9,]+)""", re.I)
PERIOD_RE = re.compile(r"""Period:\s*([0-9/\-\s]+)""", re.I)
CUSTOMER_RE = re.compile(r"""Customer:\s*(.+)""", re.I)

def parse_profile(text: str) -> Dict[str, Any]:
    fields = {}
    if m := UEI_RE.search(text): fields["uei"] = m.group(1)
    if m := DUNS_RE.search(text): fields["duns"] = m.group(1)
    if m := NAICS_RE.search(text):
        na = [n.strip() for n in m.group(1).split(",") if n.strip()]
        fields["naics"] = na
    if m := SAM_RE.search(text): fields["sam_status"] = m.group(1).lower()
    if m := EMAIL_RE.search(text): fields["poc_email"] = m.group(0)
    if m := PHONE_RE.search(text): fields["poc_phone"] = m.group(0)
    return fields

def parse_past_performance(text: str) -> Dict[str, Any]:
    fields = {}
    if m := CUSTOMER_RE.search(text): fields["customer"] = m.group(1).strip()
    if m := VALUE_RE.search(text):
        fields["value"] = int(m.group(1).replace(",", ""))
    if m := PERIOD_RE.search(text): fields["period"] = m.group(1).strip()
    if m := EMAIL_RE.search(text): fields["contact_email"] = m.group(0)
    return fields

def parse_pricing(text: str) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for line in text.strip().splitlines():
        if "," in line and "Labor" not in line:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                try:
                    rows.append({"labor_category": parts[0], "rate": float(parts[1]), "unit": parts[2]})
                except ValueError:
                    pass
    return {"rows": rows}
