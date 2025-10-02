from typing import Dict, Any
from collections import defaultdict

class MemoryStore:
    def __init__(self):
        self.docs = defaultdict(list)  # request_id -> list[dict]
        self.parsed = {}

STORE = MemoryStore()
