"""응답은 파일/fixture에서 받습니다. 네트워크 호출·SDK·API 키를 사용하지 않습니다."""
from .contracts import validate_answer
from .io import sha_text

SAFE_SUMMARIES = {
    "json_error": "JSON 문법을 확인하고 코드 블록 없이 객체 하나만 출력하세요.",
    "schema_error": "필수 네 필드·자료형·길이를 지키세요. source_ids는 양의 정수 목록입니다.",
}


def repair_prompt(original, error):
    if error not in SAFE_SUMMARIES:
        raise ValueError("형식 오류만 수정 요청을 만들 수 있습니다")
    return original + "\n[수정 요청]\n같은 질문·지식·출력 계약을 유지합니다.\n" + SAFE_SUMMARIES[error] + "\n부족한 사실을 새로 만들지 마세요."


class FixtureProvider:
    """교사가 직접 작성한 순서의 문자열 공급기. 실제 LLM이 아닙니다."""
    def __init__(self, texts):
        self.texts = list(texts)
        self.calls = 0
        self.prompts = []

    def __call__(self, prompt):
        if self.calls >= len(self.texts):
            raise ValueError("샘플이 부족합니다. 실패 원문을 임의 생성하지 않습니다")
        raw = self.texts[self.calls]
        self.calls += 1
        self.prompts.append(prompt)
        return raw


def run_with_retry(generate, prompt, validate):
    history = []
    for attempt in (1, 2):
        raw = generate(prompt)
        obj, error = validate(raw)
        # 테스트용 가상 자료만 사용합니다. 보안 검증 오류 전체는 기록/재전달하지 않습니다.
        history.append({"attempt":attempt,"error":error,"raw_text":raw,"prompt_sha256":sha_text(prompt)})
        if error is None:
            return obj, history
        if error not in {"json_error","schema_error"} or attempt == 2:
            break
        prompt = repair_prompt(prompt,error)
    return None, history


def run_fixture_scenarios(fixtures, runner=run_with_retry):
    by_id={x["fixture_id"]:x for x in fixtures}
    scenarios=[
        ("repair_success",["broken_json","valid_answer"],2,True),
        ("repair_failure",["broken_json","broken_json"],2,False),
        ("rule_stop",["unknown_source"],1,False),
        ("insufficient_stop",["valid_insufficient"],1,True),
    ]
    rows=[]
    for name, ids, calls, accepted in scenarios:
        provider=FixtureProvider([by_id[i]["raw_text"] for i in ids])
        obj,history=runner(provider,"[지식] 가상 지식101",lambda raw:validate_answer(raw,[101]))
        if provider.calls != calls or (obj is not None) != accepted:
            raise AssertionError(f"재시도 계약 불일치: {name}")
        rows.append({"scenario":name,"source_mode":"fixture","calls":provider.calls,
                     "auto_accepted":obj is not None,"evidence_ok":None,"history":history,
                     "actual_model_recovery_rate":None})
    return rows
