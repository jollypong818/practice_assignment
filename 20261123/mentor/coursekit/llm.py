"""실제 Chat Model 준비. invoke를 호출할 때 API 요청과 비용이 발생합니다."""
from coursekit.config import load_settings, require_setting

def create_chat_model():
    load_settings()
    api_key = require_setting("OPENAI_API_KEY")
    model_name = require_setting("LLM_MODEL")
    from langchain_openai import ChatOpenAI
    # 수업에서 이미 사용 가능한 Responses/Structured Output 지원 모델을 지정합니다.
    # timeout은 기다릴 시간, max_retries=1은 실패 시 추가 시도 최대 1회입니다.
    return ChatOpenAI(model=model_name, api_key=api_key, use_responses_api=True,
                      output_version="responses/v1", timeout=30, max_retries=1)

def create_generation(prompt=None, chat_model=None):
    from coursekit.checkpoints import make_prompt, WireAnswer
    prompt = make_prompt() if prompt is None else prompt
    chat_model = create_chat_model() if chat_model is None else chat_model
    structured_model = chat_model.with_structured_output(
        WireAnswer, method="json_schema", strict=True, include_raw=True)
    return prompt | structured_model
