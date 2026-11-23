"""Report Service: 6종 보고서 공통 CRUD/버전/동기화. Repository는 DB, Service는 업무 규칙."""
from datetime import datetime,date,timezone
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.core.config import settings,at_least
from app.models.report import (Report,ReportCategory,ReportEmbedding,PromptVersion,
                               DETAIL_MODELS, DETAIL_FIELDS, PromptReport)
from app.repositories import report_repository as repo
from app.integrations import embedding_client as emb
from app.integrations import llm_client
from app.services.errors import DomainError
from app.schemas.report import ReportCreate,ReportUpdate,PromptVersionCreate,DETAIL_SCHEMAS
from pydantic import ValidationError

INPUT_FIELDS={
    'EXPERIMENT':{'experiment_date','hypothesis','result_summary'},
    'DAILY_WORK':{'work_date','progress','blockers'},
    'RESEARCH_PLAN':{'research_goal','methodology','target_date'},
    'DATA_PROCESSING':{'dataset_name','processing_steps','quality_notes'},
    'PROMPT':{'purpose','prompt_text'},
    'MEETING':{'meeting_at','attendees','decisions'},
}
OPTIONAL={'DAILY_WORK':{'blockers'},'DATA_PROCESSING':{'quality_notes'}}
DATE_FIELDS={'experiment_date','work_date','target_date'}
TIME_FIELDS={'meeting_at'}


def validate_details(code:str,details:dict,content:str|None=None)->dict:
    """카테고리별 Detail 스키마. Intermediate부터 Pydantic 세부 Model로 검증합니다."""
    needed=INPUT_FIELDS.get(code)
    if needed is None:raise DomainError(422,'VALIDATION_ERROR','알 수 없는 보고서 종류입니다.')
    if not isinstance(details,dict):raise DomainError(422,'VALIDATION_ERROR','details는 객체여야 합니다.')
    required=needed-OPTIONAL.get(code,set())
    missing=required-details.keys()
    extras=details.keys()-needed
    if missing or extras:
        raise DomainError(422,'VALIDATION_ERROR',f'details 필드 누락/초과: {sorted(missing)} / {sorted(extras)}')
    result={}
    for k in needed:
        v=details.get(k,'' if k in OPTIONAL.get(code,set()) else None)
        if k in DATE_FIELDS:
            try: result[k]=date.fromisoformat(v) if isinstance(v,str) else v
            except (TypeError,ValueError):raise DomainError(422,'VALIDATION_ERROR',f'{k}는 YYYY-MM-DD 형식이어야 합니다.')
            if not isinstance(result[k],date) or isinstance(result[k],datetime):
                raise DomainError(422,'VALIDATION_ERROR',f'{k} 날짜 형식 오류')
        elif k in TIME_FIELDS:
            try: d=datetime.fromisoformat(v.replace('Z','+00:00')) if isinstance(v,str) else v
            except (TypeError,ValueError):raise DomainError(422,'VALIDATION_ERROR',f'{k} ISO 8601 형식 오류')
            if not isinstance(d,datetime) or d.tzinfo is None:
                raise DomainError(422,'VALIDATION_ERROR',f'{k}에 시간대가 필요합니다.')
            result[k]=d
        elif not isinstance(v,str) or (k not in OPTIONAL.get(code,set()) and not v.strip()):
            raise DomainError(422,'VALIDATION_ERROR',f'{k}는 비어 있지 않은 문자열이어야 합니다.')
        else: result[k]=v
    if code=='PROMPT' and content is not None and content !=result['prompt_text']:
        raise DomainError(422,'VALIDATION_ERROR','Prompt content와 details.prompt_text는 동일해야 합니다.')
    if at_least('intermediate'):
        try:
            # data validation 결과는 같은 자료형의 date/datetime 객체를 보유합니다.
            return DETAIL_SCHEMAS[code].model_validate(details).model_dump()
        except ValidationError as e:
            raise DomainError(422,'VALIDATION_ERROR','카테고리별 상세 속성을 확인하세요.') from e
    return result


def encode_overview(overview:str)->list[float]:
    try: return emb.encode([overview],kind='passage')[0]
    except Exception as e:raise DomainError(503,'EMBEDDING_UNAVAILABLE','E5 Embedding을 생성하지 못했습니다.') from e


def categories(db:Session)->dict:
    rows=db.scalars(select(ReportCategory).order_by(ReportCategory.category_id)).all()
    return {'items':[{'category_id':r.category_id,'code':r.code,'name':r.name,'description':r.description} for r in rows]}


def create_report(db:Session,data:ReportCreate)->dict:
    details=validate_details(data.category_code,data.details,data.content)
    vector=encode_overview(data.overview) # DB 트랜잭션 시작 전에 느린 외부 모델 연산 수행
    with db.begin():
        category=repo.category_for_code(db,data.category_code)
        row=Report(category_id=category.category_id,overview=data.overview,index_status='ready',revision=1)
        db.add(row);db.flush() # INSERT가 실행되어 서버가 부여한 ID 사용. commit 전에는 미확정.
        detail_kwargs={k:v for k,v in details.items() if k!='prompt_text'}
        if data.category_code=='PROMPT':detail_kwargs['active_version_no']=1
        detail=DETAIL_MODELS[data.category_code](report_id=row.report_id,title=data.title,
               content=data.content,author=data.author,**detail_kwargs)
        db.add(detail);db.flush() # PromptVersion의 FK가 참조할 Prompt 상세 행 생성.
        if data.category_code=='PROMPT':
            db.add(PromptVersion(report_id=row.report_id,version_no=1,prompt_text=details['prompt_text']))
        db.add(ReportEmbedding(report_id=row.report_id,embedding=vector,
                    model_name=settings.embedding_model,overview_hash=emb.overview_hash(data.overview),indexed_revision=1))
        rid=row.report_id
    return {'report_id':rid,'category_code':data.category_code,'title':data.title,
            'author':data.author,'revision':1,'index_status':'ready','embedding_model':settings.embedding_model}


def get_report(db:Session,rid:int)->dict:
    return repo.read_report(db,rid)


def list_reports(db:Session,title:str|None,limit:int,offset:int,
                 category_code:str|None=None,updated_after:datetime|None=None):
    return repo.list_reports(db,title,limit,offset,category_code,updated_after)


def update_report(db:Session,rid:int,data:ReportUpdate)->dict:
    # 현업 관점: E5 계산에 실패해도 기존 Report/Embedding은 그대로 있어야 합니다.
    old,cat,detail=repo.get_report_and_detail(db,rid)
    code=cat.code
    if code=='PROMPT':
        if data.content!=detail.content:
            raise DomainError(422,'VALIDATION_ERROR','Prompt 본문 변경은 활성 버전 변경 API로만 처리합니다.')
        # Prompt PUT에는 prompt_text가 아닌 purpose만 받는다. 이전 본문을 입력하면 승인.
        if set(data.details)!= {'purpose'}:
            raise DomainError(422,'VALIDATION_ERROR','Prompt PUT details에는 purpose만 지정합니다.')
        detail_data={'purpose':data.details['purpose']}
        if not isinstance(detail_data['purpose'],str) or not detail_data['purpose'].strip():
            raise DomainError(422,'VALIDATION_ERROR','purpose는 공백일 수 없습니다.')
    else:detail_data=validate_details(code,data.details,data.content)
    old_overview,old_revision=old.overview,old.revision
    old_embedding=db.get(ReportEmbedding,rid)
    # 같은 개요라도 모델·해시·Revision이 현재 상태와 맞는 벡터만 재사용합니다.
    reusable=(old.index_status=='ready' and old_embedding is not None and
              old_embedding.model_name==settings.embedding_model and
              old_embedding.overview_hash==emb.overview_hash(old_overview) and
              old_embedding.indexed_revision==old_revision)
    needs_vector=(old_overview!=data.overview or not reusable)
    # 읽기 트랜잭션을 닫고 Embedding을 계산하여 DB 연결을 불필요하게 점유하지 않습니다.
    db.rollback()
    vector=encode_overview(data.overview) if needs_vector else None
    with db.begin():
        report,cat,detail=repo.get_report_and_detail(db,rid,lock=True)
        if at_least('advanced') and data.expected_revision is not None and data.expected_revision!=report.revision:
            raise DomainError(409,'REVISION_CONFLICT','다른 요청에서 이미 보고서를 수정했습니다.')
        # 읽은 뒤 다른 요청이 개요를 바꾼 경우 계산된 벡터와 현재 데이터 불일치 방지.
        if report.overview!=old_overview or report.revision!=old_revision:
            raise DomainError(409,'REVISION_CONFLICT','수정 중 보고서가 변경되었습니다. 다시 조회하세요.')
        target=db.get(ReportEmbedding,rid)
        # 잠금을 얻기 전 인덱스 상태가 바뀌었다면 잘못된 벡터를 ready로 승격하지 않습니다.
        if not needs_vector and (report.index_status!='ready' or target is None or
                target.model_name!=settings.embedding_model or
                target.overview_hash!=emb.overview_hash(report.overview) or
                target.indexed_revision!=report.revision):
            raise DomainError(409,'REVISION_CONFLICT','수정 중 인덱스 상태가 변경되었습니다. 다시 조회하세요.')
        for k in ('title','author','content'):setattr(detail,k,getattr(data,k))
        for k,v in detail_data.items():setattr(detail,k,v)
        detail.update_at=datetime.now(timezone.utc)
        report.overview=data.overview
        report.revision+=1
        if needs_vector:
            if target is None:
                target=ReportEmbedding(report_id=rid);db.add(target)
            target.embedding=vector
            target.model_name=settings.embedding_model
            target.overview_hash=emb.overview_hash(data.overview)
            target.indexed_at=datetime.now(timezone.utc)
        target.indexed_revision=report.revision
        report.index_status='ready'
        revision=report.revision
    return {'report_id':rid,'revision':revision,'index_status':'ready','embedding_updated':needs_vector}


def delete_report(db:Session,rid:int)->None:
    with db.begin():
        report=db.get(Report,rid)
        if report is None:raise DomainError(404,'REPORT_NOT_FOUND','보고서가 없습니다.')
        db.delete(report) # PostgreSQL ON DELETE CASCADE가 상세·Embedding·Prompt 버전을 제거


def summarize_report(db:Session,rid:int,style:str='brief',max_sentences:int=3)->dict:
    record=repo.read_report(db,rid)
    result=llm_client.summarize(record['content'],style,max_sentences,allow_structured=at_least('intermediate'),
                                retries=2 if at_least('advanced') else 0)
    payload={'report_id':rid,'source_revision':record['revision'],**result,
            'model':settings.llm_model,'status':'completed'}
    if at_least('advanced') and llm_client.get_last_usage() is not None:
        payload['usage']=llm_client.get_last_usage()
    return payload


def prompt_add_version(db:Session,rid:int,prompt_text:str)->dict:
    if not at_least('intermediate'):
        raise DomainError(422,'VALIDATION_ERROR','Prompt 버전 추가는 Intermediate 기능입니다.')
    with db.begin():
        report,cat,detail=repo.get_report_and_detail(db,rid,lock=True)
        if cat.code!='PROMPT':raise DomainError(422,'NOT_PROMPT_REPORT','프롬프트 보고서만 허용합니다.')
        maxver=db.scalar(select(func.max(PromptVersion.version_no)).where(PromptVersion.report_id==rid)) or 0
        nextver=maxver+1
        db.add(PromptVersion(report_id=rid,version_no=nextver,prompt_text=prompt_text))
    return {'version_no':nextver,'active':False}


def prompt_list_versions(db:Session,rid:int)->dict:
    if not at_least('intermediate'):
        raise DomainError(422,'VALIDATION_ERROR','Prompt 버전 조회는 Intermediate 기능입니다.')
    report,cat,detail=repo.get_report_and_detail(db,rid)
    if cat.code!='PROMPT':raise DomainError(422,'NOT_PROMPT_REPORT','프롬프트 보고서만 허용합니다.')
    versions=db.scalars(select(PromptVersion).where(PromptVersion.report_id==rid)
                        .order_by(PromptVersion.version_no)).all()
    return {'items':[{'version_no':v.version_no,'created_at':repo.plain_value(v.created_at)} for v in versions],
            'active_version_no':detail.active_version_no}

