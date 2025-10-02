from fastapi import APIRouter, HTTPException
from ..core.schemas import IngestRequest, IngestResponse, DocSummary
from ..core.pii import redact
from ..core.storage import STORE
import uuid

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
def ingest(payload: IngestRequest):
    if len(payload.documents) > 50:
        raise HTTPException(status_code=400, detail="Too many documents")
    req_id = str(uuid.uuid4())
    summaries = []
    for d in payload.documents:
        red = redact(d.text)
        STORE.docs[req_id].append({"name": d.name, "type_hint": d.type_hint, "text": red})
        summaries.append(DocSummary(name=d.name, type_hint=d.type_hint, char_len=len(d.text)))
    return IngestResponse(doc_summaries=summaries, request_id=req_id)
