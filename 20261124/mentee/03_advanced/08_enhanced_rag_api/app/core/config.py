"""환경 설정은 coursekit.config에서 검증. 이 파일은 API 계층 진입점만 맡습니다."""
from coursekit.config import require_cuda,require_setting,schema_name

def validate_runtime():
    return {'device':require_cuda(),'schema':schema_name(),
            'llm_model':require_setting('LLM_MODEL')}
