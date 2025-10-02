from typing import Dict, Any, List
from .vectorstore import TinyVectorStore
from .rules_pack import RULES
from .utils import map_naics_to_sin, within_last_36_months

def build_checklist(extracted: Dict[str, Any], rules_to_use: Dict[str,str] = None) -> Dict[str, Any]:
    idx = TinyVectorStore(rules_to_use or RULES)
    problems = []
    citations = []

    # --- Identity & Registry (R1)
    r1 = idx.retrieve(["UEI","DUNS","SAM"], k=1)
    if r1:
        citations.append({"rule_id": r1[0][0], "chunk": r1[0][1]})
        if not extracted.get("profile", {}).get("uei"):
            problems.append({"code": "missing_uei", "evidence": "UEI not found in profile", "rules": [r1[0][0]]})
        if not extracted.get("profile", {}).get("duns"):
            problems.append({"code": "missing_duns", "evidence": "DUNS not found in profile", "rules": [r1[0][0]]})
        if extracted.get("profile", {}).get("sam_status", "") not in {"active","registered"}:
            problems.append({"code": "sam_not_active", "evidence": f"SAM status: {extracted.get('profile',{}).get('sam_status')}", "rules": [r1[0][0]]})
        if not extracted.get("profile", {}).get("poc_email"):
            problems.append({"code": "missing_poc_email", "evidence": "POC email missing", "rules": [r1[0][0]]})
        if not extracted.get("profile", {}).get("poc_phone"):
            problems.append({"code": "missing_poc_phone", "evidence": "POC phone missing", "rules": [r1[0][0]]})
    else:
        problems.append({"code": "needs_human", "evidence": "R1 not available in index", "rules": []})

    # --- NAICS & SIN (R2)
    r2 = idx.retrieve(["NAICS","SIN"], k=1)
    if r2 and extracted.get("profile", {}).get("naics"):
        citations.append({"rule_id": r2[0][0], "chunk": r2[0][1]})
        mapped = map_naics_to_sin(extracted["profile"]["naics"])
        extracted.setdefault("profile", {})["sin"] = mapped

    # --- Past Performance (R3)
    r3 = idx.retrieve(["past performance","value","email"], k=1)
    if r3:
        citations.append({"rule_id": r3[0][0], "chunk": r3[0][1]})
        pps: List[Dict[str,Any]] = extracted.get("past_performance", [])
        if not pps:
            problems.append({"code": "no_past_performance", "evidence": "No PP docs", "rules": [r3[0][0]]})
        else:
            ok_any = False
            for pp in pps:
                if pp.get("value", 0) >= 25000 and pp.get("contact_email") and within_last_36_months(pp.get("period","")):
                    ok_any = True
            if not ok_any:
                problems.append({"code": "past_performance_min_value_not_met", "evidence": "No PP >= $25,000 within last 36 months with email", "rules": [r3[0][0]]})

    # --- Pricing (R4)
    r4 = idx.retrieve(["pricing","rates","unit"], k=1)
    if r4:
        citations.append({"rule_id": r4[0][0], "chunk": r4[0][1]})
        rows = extracted.get("pricing", {}).get("rows", [])
        if not rows or any(not r.get("unit") for r in rows):
            problems.append({"code": "pricing_incomplete", "evidence": "Missing unit/rate basis", "rules": [r4[0][0]]})

    # --- Submission Hygiene (R5)
    r5 = idx.retrieve(["PII","redacted","stored"], k=1)
    if r5:
        citations.append({"rule_id": r5[0][0], "chunk": r5[0][1]})

    required_ok = not any(p for p in problems if p["code"] in {"missing_uei","missing_duns","sam_not_active","past_performance_min_value_not_met","pricing_incomplete"})
    return {"required": required_ok, "problems": problems, "citations": citations}
