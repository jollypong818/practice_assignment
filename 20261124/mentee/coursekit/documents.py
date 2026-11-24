"""기존 Day26 Hit ↔ LangChain Document 변환. 필수 출처를 지우거나 임의로 생성하지 않습니다."""
META_KEYS = ('citation_id', 'chunk_id', 'doc_id', 'source_version',
             'source_locator', 'category', 'access_level', 'ready', 'is_current')


def hit_to_document(hit):
    from langchain_core.documents import Document
    required=('body','citation_id','chunk_id','doc_id','source_version','source_locator','category')
    missing=[key for key in required if key not in hit]
    if missing:
        raise ValueError(f'Hit 필수 필드 누락: {missing}')
    if not str(hit['body']).strip():
        raise ValueError('빈 본문은 Document에 넣지 않습니다.')
    metadata={key:hit[key] for key in META_KEYS if key in hit}
    for key in ('title','cosine_distance','found_by_query'):
        if key in hit:metadata[key]=hit[key]
    return Document(page_content=hit['body'],metadata=metadata)


def valid_document(doc):
    if not getattr(doc,'page_content','').strip():
        raise ValueError('Document 본문이 비었습니다.')
    metadata=doc.metadata
    for key in ('chunk_id','doc_id','source_locator','category','citation_id'):
        if key not in metadata:
            raise ValueError(f'Document Metadata 누락: {key}')
    if type(metadata['citation_id']) is not int or metadata['citation_id']<=0:
        raise ValueError('citation_id는 실제 DB/Fixture가 만든 양의 정수이어야 합니다.')
    return doc


def docs_to_ids(docs):return [valid_document(d).metadata['chunk_id'] for d in docs]


def context_from_documents(docs, *, context_k=2, max_chars=650):
    if type(context_k) is not int or not 1<=context_k<=3:raise ValueError('context_k: 1~3')
    if type(max_chars) is not int or max_chars<1:raise ValueError('max_chars: positive int')
    blocks,included,seen=[],[],set()
    for doc in docs:
        valid_document(doc)
        cid=doc.metadata['chunk_id']
        if cid in seen:continue
        seen.add(cid)
        block=f'[{doc.metadata["citation_id"]}] {doc.metadata["source_locator"]}\n{doc.page_content}'
        if len('\n\n'.join(blocks+[block]))>max_chars:continue
        blocks.append(block);included.append(doc)
        if len(included)>=context_k:break
    return '\n\n'.join(blocks),included


def source_index(included):
    result={}
    for doc in included:
        valid_document(doc)
        cid=doc.metadata['citation_id']
        if cid in result:raise ValueError('중복 citation_id는 반환할 수 없습니다.')
        result[cid]={key:doc.metadata[key] for key in
                     ('citation_id','chunk_id','doc_id','source_version','source_locator','category')}
    return result
