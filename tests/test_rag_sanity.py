from backend.app.core.rag import build_checklist
from backend.app.core.rules_pack import RULES

def test_rag_sanity_missing_R1():
    # remove R1 from index
    rules_wo_r1 = {k:v for k,v in RULES.items() if k != "R1"}
    extracted = {"profile": {"duns":"123456789","sam_status":"registered"}, "past_performance": [], "pricing": {}}
    checklist = build_checklist(extracted, rules_to_use=rules_wo_r1)
    # should NOT cite R1 in any citation and ideally add needs_human
    codes = {p["code"] for p in checklist["problems"]}
    assert "needs_human" in codes
    for c in checklist.get("citations", []):
        assert c["rule_id"] != "R1"
