from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..core.schemas import AnalyzeResponse
from ..core.storage import STORE
from ..core.classification import classify
from ..core.extraction import parse_profile, parse_past_performance, parse_pricing
from ..core.rag import build_checklist
from ..core.rules_pack import RULES

router = APIRouter()

def _analyze_docs(docs) -> Dict[str, Any]:
    extracted: Dict[str, Any] = {"profile": {}, "past_performance": [], "pricing": {}}
    for d in docs:
        kind = d.get("type_hint") or classify(d["text"])
        if kind == "profile":
            extracted["profile"].update(parse_profile(d["text"]))
        elif kind == "past_performance":
            extracted["past_performance"].append(parse_past_performance(d["text"]))
        elif kind == "pricing":
            extracted["pricing"] = parse_pricing(d["text"])
        else:
            # unknown -> ignore, but could be surfaced for human review
            pass
    return extracted

def _generate_brief(checklist: Dict[str,Any]) -> str:
    probs = ", ".join(p["code"] for p in checklist["problems"]) or "none"
    return (
        "Negotiation Prep Brief:\n"
        f"Strengths: Clear structure and initial data provided.\n"
        f"Weaknesses: {probs}. Use rule citations to guide requests."
    )

def _generate_client_email(checklist: Dict[str,Any]) -> str:
    lines = ["Subject: Follow-up on GSA Onboarding Items",
             "Hi team,",
             "Thanks for sharing the onboarding materials. We reviewed them against GSA policy."]
    if checklist["problems"]:
        lines.append("We need the following to proceed:")
        for p in checklist["problems"]:
            rid = p.get("rules", ["R?"])[0]
            lines.append(f"- {p['code']} ({rid}) — {p['evidence']}")
    else:
        lines.append("We're all set based on the current materials.")
    lines.append("Best regards,")
    lines.append("GetGSA Bot")
    return "\n".join(lines)

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request_id: str):
    docs = STORE.docs.get(request_id)
    if not docs:
        raise HTTPException(status_code=404, detail="request_id not found or empty")
    extracted = _analyze_docs(docs)
    checklist = build_checklist(extracted, RULES)
    citations = checklist.get("citations", [])
    brief = _generate_brief(checklist)
    email = _generate_client_email(checklist)
    STORE.parsed[request_id] = {"extracted": extracted, "checklist": checklist}
    return {
        "parsed": extracted,
        "checklist": {"required": checklist["required"], "problems": checklist["problems"]},
        "brief": brief,
        "client_email": email,
        "citations": citations,
        "request_id": request_id,
    }
