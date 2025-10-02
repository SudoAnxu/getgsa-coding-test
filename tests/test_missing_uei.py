from backend.app.core.rag import build_checklist

def test_missing_uei():
    extracted = {"profile": {"duns":"123456789","sam_status":"registered"}, "past_performance": [], "pricing": {}}
    checklist = build_checklist(extracted)
    codes = {p["code"] for p in checklist["problems"]}
    assert "missing_uei" in codes
