from typing import Dict, List, Tuple
from .rules_pack import RULES

class TinyVectorStore:
    def __init__(self, rules: Dict[str, str] = None):
        self.rules = dict(rules or RULES)

    def remove(self, rule_id: str):
        if rule_id in self.rules:
            del self.rules[rule_id]

    def retrieve(self, query_terms: List[str], k: int = 3) -> List[Tuple[str, str]]:
        # naive: score by term overlap
        scored = []
        for rid, txt in self.rules.items():
            score = sum(txt.lower().count(t.lower()) for t in query_terms)
            if score > 0:
                scored.append((rid, txt, score))
        scored.sort(key=lambda x: x[2], reverse=True)
        return [(rid, txt) for rid, txt, _ in scored[:k]]

    def all(self):
        return self.rules.copy()
