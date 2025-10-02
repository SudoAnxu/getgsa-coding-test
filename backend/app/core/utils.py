from typing import List, Dict

NAICS_TO_SIN = {
    "541511": "54151S",
    "541512": "54151S",
    "541611": "541611",
    "518210": "518210C",
}

def map_naics_to_sin(naics: List[str]) -> List[str]:
    mapped = {NAICS_TO_SIN.get(n.strip(), None) for n in naics}
    return sorted([m for m in mapped if m])

def within_last_36_months(period: str) -> bool:
    # naive: assume provided periods are within 36 months for sample;
    # real impl would parse dates.
    return True
