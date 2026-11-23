"""현재 역할 폴더의 .env만 읽습니다. 자격 증명 값을 출력하지 않습니다."""
from pathlib import Path
import os
import re
from coursekit.io import ROOT

def load_settings():
    from dotenv import load_dotenv
    # 이미 터미널에 설정한 값이 있으면 덮어쓰지 않습니다.
    load_dotenv(ROOT / ".env", override=False, encoding="utf-8")

def require_setting(name):
    value = os.getenv(name, "").strip()
    if not value or value.startswith("CHANGE_ME"):
        raise RuntimeError(f"{name} 설정이 필요합니다. {ROOT / '.env.example'}을 참고해 {ROOT / '.env'}에 입력하세요.")
    return value

def schema_name():
    name = os.getenv("RAG_SCHEMA", "d26_rag").strip()
    if not re.fullmatch(r"d26_[a-z0-9_]{1,50}", name):
        raise ValueError("RAG_SCHEMA는 d26_로 시작하는 영문 소문자·숫자·밑줄 이름이어야 합니다.")
    return name

def db_parameters():
    load_settings()
    return dict(host=os.getenv("PGHOST", "localhost"), port=int(os.getenv("PGPORT", "5432")),
                dbname=os.getenv("PGDATABASE", "knowledge_lab"), user=os.getenv("PGUSER", "postgres"),
                password=require_setting("PGPASSWORD"), connect_timeout=10)
