from backend.app.core.rag import build_checklist

def test_pp_threshold():
    extracted = {
        "profile": {"uei":"ABC123DEF456","duns":"123456789","sam_status":"registered"},
        "past_performance": [ {"customer":"X","value": 18000,"period":"07/2023 - 03/2024","contact_email":"x@y.com"} ],
        "pricing": {}
    }
    checklist = build_checklist(extracted)
    codes = {p["code"] for p in checklist["problems"]}
    assert "past_performance_min_value_not_met" in codes
