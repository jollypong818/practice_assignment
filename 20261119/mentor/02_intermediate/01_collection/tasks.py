"""실습 01 Intermediate · run via python main.py"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,save_json,show_success,load_json
from coursekit.documents import raw_path,sha_bytes


def sort_rows(rows:list[dict])->list[dict]:
    # BEGIN D24-01-I01
    # 개념·실무 해설: 원본 수집 시 경로가 존재하는지 확인하고 read_bytes()를 사용합니다. text decode는 다음 실습에서 수행하므로 이 단계에서 원문 바이트를 바꾸지 않습니다.
    # 해설 D24-01-I01 : 문서 목록을 doc_id 순으로 정렬합니다. 동일 ID가 있으면 오류로 분류합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    ids=[r['doc_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate doc ID')
    return sorted(rows,key=lambda r:r['doc_id'])
    # END D24-01-I01


def classify(path:Path)->str:
    # BEGIN D24-01-I02
    # 개념·실무 해설: len(raw)은 Byte 길이이며 len(text)와 같지 않습니다. SHA-256은 같은 바이트를 다시 확인하기 위한 식별 단서이지 문서의 내용이 진실임을 증명하지 않습니다.
    # 해설 D24-01-I02 : 확장자와 허용 집합을 비교하여 supported/unsupported를 반환합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return 'supported' if path.suffix.lower() in {'.txt','.md','.html','.pdf'} else 'unsupported'
    # END D24-01-I02


def collect_one(doc:dict)->dict:
    # BEGIN D24-01-I03
    # 개념·실무 해설: 문서 ID와 파일명은 다른 계약입니다. 원본 이름이 변경되어도 동일 문서의 이력을 doc_id로 이어갈 수 있어야 합니다.
    # 해설 D24-01-I03 : 파일별 원문 크기·해시 또는 읽기 실패 이유를 안전하게 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    path=raw_path(doc)
    result={'doc_id':doc['doc_id'],'file':doc['file'],'version':doc['source_version'],
            'category':doc['category'],'status':classify(path)}
    if result['status']=='unsupported':return result
    try:raw=path.read_bytes()
    except OSError as exc:
        result.update(status='read_error',reason=type(exc).__name__)
    else:
        result.update(status='collected',size_bytes=len(raw),raw_sha256=sha_bytes(raw))
    return result
    # END D24-01-I03


def collect_all(rows:list[dict])->dict:
    # BEGIN D24-01-I04
    # 개념·실무 해설: 지원 밖 확장자를 조용히 제외하면 입력 총수가 줄어듭니다. unsupported와 read_error는 별도의 상태로 남깁니다.
    # 해설 D24-01-I04 : 모든 입력을 제외 없이 기록하고 상태별 건수 합이 입력 수와 일치하는지 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    items=[collect_one(r) for r in sort_rows(rows)]
    counts={state:sum(r['status']==state for r in items)
            for state in ('collected','unsupported','read_error')}
    assert sum(counts.values())==len(items)
    return {'total':len(items),'counts':counts,'items':items}
    # END D24-01-I04


def main():
    result=collect_all(load_json(DATA/'manifest.json'))
    out=save_json(HERE,'manifest_report.json',result)
    show_success('01 Intermediate',out)
