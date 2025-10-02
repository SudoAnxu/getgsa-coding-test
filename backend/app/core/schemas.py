from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IngestDoc(BaseModel):
    name: str
    type_hint: Optional[str] = None
    text: str

class IngestRequest(BaseModel):
    documents: List[IngestDoc]

class DocSummary(BaseModel):
    name: str
    type_hint: Optional[str] = None
    char_len: int

class IngestResponse(BaseModel):
    doc_summaries: List[DocSummary]
    request_id: str

class AnalyzeResponse(BaseModel):
    parsed: Dict[str, Any]
    checklist: Dict[str, Any]
    brief: str
    client_email: str
    citations: List[Dict[str, Any]]
    request_id: str
