"""환경 설정. 실제 비밀번호와 API 키는 .env에만 두고 Git에 올리지 않습니다."""
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / '.env', override=False)

@dataclass(frozen=True)
class Settings:
    # 운영 원칙: 설정은 프로젝트 밖에 공유하지 않고 로그에도 출력하지 않습니다.
    database_url: str = os.getenv('DATABASE_URL', '')
    embedding_model: str = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-small')
    search_min_similarity: float = float(os.getenv('SEARCH_MIN_SIMILARITY','0.75'))
    llm_model: str = os.getenv('LLM_MODEL','')
    llm_timeout: float = float(os.getenv('LLM_TIMEOUT_SECONDS','30'))
    llm_max_tokens: int = int(os.getenv('LLM_MAX_OUTPUT_TOKENS','400'))
    project_level: str = os.getenv('PROJECT_LEVEL', 'basic').lower()

settings = Settings()

def at_least(level: str) -> bool:
    order = {'basic':1,'intermediate':2,'advanced':3}
    return order.get(settings.project_level,1)>=order[level]
