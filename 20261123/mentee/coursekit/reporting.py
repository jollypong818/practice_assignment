"""결과 관찰용 직렬화. 실측과 고정 교육 예시의 실행 여부를 구분합니다."""

def message_record(message):
    return {"type": type(message).__name__, "text": message.text,
            "response_metadata": message.response_metadata,
            "usage_metadata": message.usage_metadata}

def bundle_record(bundle):
    raw, parsed, error = bundle["raw"], bundle["parsed"], bundle["parsing_error"]
    return {"raw": message_record(raw),
            "parsed": parsed.model_dump() if hasattr(parsed, "model_dump") else parsed,
            "parsing_error": None if error is None else type(error).__name__ + ": " + str(error)}

def execution_record(mode, *, db=False, embedding=False, llm=False):
    return {"mode": mode, "db": bool(db), "embedding": bool(embedding), "llm": bool(llm)}
