"""실습 01 Advanced · 원문 스냅샷과 변경 추적."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json,save_json,show_success
from coursekit.documents import raw_path,sha_bytes


def validate_manifest(rows:list[dict])->list[dict]:
    # BEGIN D24-01-A01
    # 개념·실무 해설: 원본 수집 시 경로가 존재하는지 확인하고 read_bytes()를 사용합니다. text decode는 다음 실습에서 수행하므로 이 단계에서 원문 바이트를 바꾸지 않습니다.
    # 해설 D24-01-A01 : 입력 manifest의 필수 필드·중복 ID·허용 형식과 경로 계약을 검증합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    ids=set();out=[]
    for row in rows:
        for key in ('doc_id','file','category','source_version'):
            if not isinstance(row.get(key),str) or not row[key].strip():raise ValueError('missing '+key)
        if row['doc_id'] in ids:raise ValueError('duplicate doc_id')
        ids.add(row['doc_id'])
        if Path(row['file']).name!=row['file'] or Path(row['file']).is_absolute():
            raise ValueError('untrusted filename')
        out.append(row)
    return sorted(out,key=lambda row:row['doc_id'])
    # END D24-01-A01


def collect_one(row:dict)->dict:
    # BEGIN D24-01-A02
    # 개념·실무 해설: len(raw)은 Byte 길이이며 len(text)와 같지 않습니다. SHA-256은 같은 바이트를 다시 확인하기 위한 식별 단서이지 문서의 내용이 진실임을 증명하지 않습니다.
    # 해설 D24-01-A02 : 원문을 수집하여 bytes 길이·raw_sha256 또는 명시적 오류를 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    path=raw_path(row)
    info={'doc_id':row['doc_id'],'source_version':row['source_version'],'file':row['file']}
    if path.suffix.lower() not in {'.txt','.md','.html','.pdf'}:
        return {**info,'status':'unsupported','reason':'extension'}
    try:raw=path.read_bytes()
    except OSError as exc:return {**info,'status':'read_error','reason':type(exc).__name__}
    return {**info,'status':'collected','size_bytes':len(raw),'raw_sha256':sha_bytes(raw)}
    # END D24-01-A02


def compare_version(record:dict,previous:dict|None)->str:
    # BEGIN D24-01-A03
    # 개념·실무 해설: 문서 ID와 파일명은 다른 계약입니다. 원본 이름이 변경되어도 동일 문서의 이력을 doc_id로 이어갈 수 있어야 합니다.
    # 해설 D24-01-A03 : 이전 해시와 현재 해시로 new·unchanged·changed·unreadable을 구분합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if record['status']!='collected':return 'unreadable'
    if previous is None:return 'new'
    return 'unchanged' if previous.get('raw_sha256')==record['raw_sha256'] else 'changed'
    # END D24-01-A03


def failure_audit(records:list[dict])->list[dict]:
    # BEGIN D24-01-A04
    # 개념·실무 해설: 지원 밖 확장자를 조용히 제외하면 입력 총수가 줄어듭니다. unsupported와 read_error는 별도의 상태로 남깁니다.
    # 해설 D24-01-A04 : 지원하지 않는 형식과 파일 접근 실패를 감사 목록에 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return [{'doc_id':r['doc_id'],'status':r['status'],'reason':r.get('reason')}
            for r in records if r['status']!='collected']
    # END D24-01-A04


def reconcile(records:list[dict])->dict:
    # BEGIN D24-01-A05
    # 개념·실무 해설: 집계의 합이 원래 입력 수와 일치해야 수집 누락을 탐지할 수 있습니다. 실패도 분모에 포함시킵니다.
    # 해설 D24-01-A05 : 입력 건수 = 수집·미지원·읽기 오류 건수인지 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    by={s:sum(r['status']==s for r in records)
        for s in ('collected','unsupported','read_error')}
    if len(records)!=sum(by.values()):raise ValueError('lost or unknown status')
    return {'input_count':len(records),'by_status':by,'failures':failure_audit(records)}
    # END D24-01-A05


def fingerprint(records:list[dict])->str:
    # BEGIN D24-01-A06
    # 개념·실무 해설: 정해진 ID 순서와 JSON 직렬화 규칙으로 동일 파일의 fingerprint를 고정합니다. 재실행으로 값이 바뀌면 입력/설정이 달라졌는지 조사합니다.
    # 해설 D24-01-A06 : 같은 파일·같은 순서 재실행 시 안정적인 manifest fingerprint를 계산합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    canonical=json.dumps(records,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    # END D24-01-A06


def main():
    rows=validate_manifest(load_json(DATA/'manifest.json'))
    records=[collect_one(r) for r in rows]
    report=reconcile(records)
    report['fingerprint']=fingerprint(records)
    report['repeat_equal']=fingerprint([collect_one(r) for r in rows])==report['fingerprint']
    changed={**records[0],'raw_sha256':'0'*64}
    report['change_example']=compare_version(records[0],changed)
    out=save_json(HERE,'collection_audit.json',report)
    show_success('01 Advanced',out)
