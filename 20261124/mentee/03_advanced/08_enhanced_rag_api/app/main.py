"""Uvicorn app factory. import만으로 GPU/DB/LLM을 호출하지 않습니다."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))

def create_app_factory():
    """실제 GPU/DB/LLM 준비는 ASGI factory 호출 시에만 실행됩니다."""
    from app.retrieval.stages import make_service_chain
    from app.services.rag_service import wire_fastapi
    return wire_fastapi(make_service_chain(offline=False))
