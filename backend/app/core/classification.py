from typing import Literal

def classify(text: str) -> Literal["profile","past_performance","pricing","unknown"]:
    t = text.lower()
    scores = {
        "profile": sum(kw in t for kw in ["uei", "duns", "naics", "sam.gov", "poc"]),
        "past_performance": sum(kw in t for kw in ["customer:", "period:", "value:", "contact:"]),
        "pricing": sum(kw in t for kw in ["labor category", "rate", "unit"]),
    }
    best = max(scores, key=scores.get)
    if scores[best] == 0 or list(scores.values()).count(scores[best]) > 1:
        return "unknown"
    return best
