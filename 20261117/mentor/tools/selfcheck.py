"""네트워크 없이 공통 기능과 패키지 상태를 점검합니다. TODO 정답 검사는 아닙니다."""
from pathlib import Path
import ast
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coursekit.io import ROOT, input_parts, read_json
from coursekit.config import load_settings
from coursekit.runner import run_request
from coursekit.request import build_request
from coursekit.labs import failure_scenarios


def main():
    checked = 0
    for path in ROOT.rglob("*.py"):
        if any(part in {".venv", "__pycache__", "outputs"} for part in path.parts):
            continue
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        checked += 1
    settings = load_settings("simulated")  # API 키나 .env를 읽지 않습니다.
    for case_id in ("H01", "H02", "H03"):
        case, selected, instructions = input_parts(case_id)
        request = build_request(settings.models["fast"], instructions, case["question"], selected)
        result = run_request(request, set(case["selected_ids"]), source="simulated", settings=settings,
                             case_id=case_id, stream=case_id == "H01")
        assert result["source_mode"] == "simulated"
        assert result["run_status"] == "validated"
        assert result["evidence_ok"] is None
        assert result["new_api_send_count"] == 0
    print(f"Python 구문 {checked}개와 제공 공통 호출·검증 흐름 확인 완료")
    print("실제 API 전송: 0회. SDK/인증/모델 권한/실제 응답 품질은 검증하지 않았습니다.")
    print("각 교시의 TODO는 별도로 완성하고 해당 main.py를 실행하세요.")


if __name__ == "__main__":
    main()
