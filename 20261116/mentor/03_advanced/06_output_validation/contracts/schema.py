"""PPT 50: 모델 정의만 담당합니다."""
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

def make_model():
    # 해설 D21-06-A01: PPT 50장의 엄격한 네 필드 계약을 선언하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 문자열 ID "101", bool true, 추가 필드, 501자 답을 거부합니다.
    # 핵심: 모델 정의는 로컬 검증입니다. 실제 LLM의 생성 형식을 자동 제약하는 API 설정은 아닙니다.
    # BEGIN D21-06-A01
    SourceID=Annotated[int,Field(strict=True,gt=0)]
    class KnowledgeAnswer(BaseModel):
        model_config=ConfigDict(extra="forbid",strict=True)
        status: Literal["answered","insufficient_context"]
        answer: str = Field(min_length=1,max_length=500)
        source_ids: list[SourceID] = Field(max_length=3)
        missing_information: str = Field(max_length=200)
    # END D21-06-A01
    return KnowledgeAnswer
