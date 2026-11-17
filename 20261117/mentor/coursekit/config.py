"""키·모델 설정. .env는 role 폴더의 한 곳만 읽고 값은 기록하지 않습니다."""
from dataclasses import dataclass, field
from pathlib import Path
import os
import math
from .io import ROOT, read_json


class SetupError(Exception):
    """상세 오류에 키를 넣지 않는 안전한 설정 오류."""


@dataclass(frozen=True)
class Settings:
    api_key: str = field(repr=False)
    models: dict = field(default_factory=dict)
    timeout_s: float = 30.0
    max_output_tokens: int = 1200
    max_live_sends: int = 20
    scope: str = "classroom-demo"


def load_settings(source, *, require_key=True):
    if source not in {"live", "simulated"}:
        raise SetupError("source는 live 또는 simulated입니다")
    # 모의 경로에서는 .env와 API 키를 읽지 않습니다.
    env = {}
    if source == "live":
        env_path = ROOT / ".env"
        if env_path.exists():
            try:
                from dotenv import dotenv_values
            except ImportError:
                raise SetupError("python-dotenv를 설치하거나 OS 환경변수만 사용하세요") from None
            env.update(dotenv_values(env_path))
        for key in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_MODEL_QUALITY", "DAY22_SCOPE", "DAY22_MAX_LIVE_SENDS"):
            if key in os.environ:
                env[key] = os.environ[key]  # OS 환경변수가 .env보다 우선합니다.
    profiles = read_json(ROOT / "config" / "models.json")
    fast = env.get("OPENAI_MODEL") or profiles["fast"]["model"]
    quality = env.get("OPENAI_MODEL_QUALITY") or (profiles["quality"]["model"] if source == "simulated" else None)
    known = {item["model"] for item in profiles.values()}
    if fast not in known or (quality is not None and quality not in known):
        raise SetupError("모델을 변경하려면 models.json의 지원 설정과 prices.json을 함께 확인하세요")
    key = env.get("OPENAI_API_KEY") or ""
    if source == "live" and require_key and (not key.strip() or key in {"YOUR_API_KEY", "본인_키"}):
        raise SetupError("API 키가 미설정입니다. .env.example을 복사해 본인 PC에서 설정하세요")
    try:
        limit = int(env.get("DAY22_MAX_LIVE_SENDS") or "20")
    except ValueError:
        raise SetupError("DAY22_MAX_LIVE_SENDS는 양의 정수입니다") from None
    if not 1 <= limit <= 100:
        raise SetupError("수업 호출 상한은 1~100 범위에서 강사 승인 후 설정합니다")
    scope = env.get("DAY22_SCOPE") or "classroom-demo"
    if not scope.strip():
        raise SetupError("scope가 비어 있습니다")
    return Settings(key, {"fast": fast, "quality": quality}, max_live_sends=limit, scope=scope)


def choose_model(mode, models):
    if mode not in {"fast", "quality"}:
        raise SetupError("지원하지 않는 실행 모드: 전송하지 않습니다")
    if not models.get(mode):
        raise SetupError("quality 모델은 미설정입니다. 권한 확인 후 설정하며 자동 대체하지 않습니다")
    return models[mode], f"explicit_mode:{mode}"
