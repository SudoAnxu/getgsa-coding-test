from fastapi import FastAPI
from .api.routes_health import router as health_router
from .api.routes_ingest import router as ingest_router
from .api.routes_analyze import router as analyze_router

app = FastAPI(title="GetGSA API", version="0.1.0")
app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(analyze_router)
