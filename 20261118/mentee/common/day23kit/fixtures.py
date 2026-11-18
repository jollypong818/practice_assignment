"""로컬 설명용 모의 벡터. 실제 E5 모델·실측 품질이 아닙니다.

384차원 배열이 필요할 때에는 교육용 2차원 좌표를 앞에 두고
나머지 382개를 0으로 둡니다. 이 벡터를 PostgreSQL에 저장하지 마세요.
"""
from __future__ import annotations
import numpy as np
from .data import load_knowledge, DIMS, passage_text

POINTS = {
   101:(1.,0.), 102:(.8,.6), 103:(0.,1.), 104:(.9,-.2),
   105:(.65,-.35), 106:(.76,.5), 107:(.71,.4),
   108:(-.1,.98),109:(-.6,.8)
}
QUERIES = {
  "서버는 어디에서 실행하나요?":(0.8,0.6),
  "서버를 어디서 켜나요?":(0.8,0.6),
  "실습 파일은 어디에 보관하나요?":(1.,0.),
  "실습 파일은 몇 년 동안 보관하나요?":(1.,0.),
  "오류를 질문할 때 무엇을 적어야 하나요?":(0.,1.),
  "회사 비밀번호는 무엇인가요?":(0.8,0.6),
}

def fixture_vec(point):
    v = np.zeros(DIMS, dtype=np.float32)
    v[:2] = point
    size = np.linalg.norm(v)
    if size == 0: raise ValueError('fixture 영벡터')
    return v / size

def doc_vector(row):
    return fixture_vec(POINTS[row['id']])

def fixture_query(question):
    return fixture_vec(QUERIES.get(question, (-0.4,0.9)))

class SimulatedEncoder:
    model_id = "SIMULATED_2D_PADDED_TO_384_NOT_E5"
    source_mode = "simulated"
    max_seq_length = 512
    def get_sentence_embedding_dimension(self): return DIMS
    def encode(self, texts, normalize_embeddings=True, convert_to_numpy=True, batch_size=8):
        if isinstance(texts, str): texts = [texts]
        rows = load_knowledge(); lookups = {passage_text(r):r for r in rows}
        result = []
        for item in texts:
            if item in lookups:
                result.append(doc_vector(lookups[item]))
            elif item.startswith("query: "):
                result.append(fixture_query(item[len("query: "):]))
            else:
                raise ValueError('모의 Encoder 입력 계약이 다릅니다: query:/passage:')
        arr=np.stack(result) if result else np.empty((0,DIMS),dtype=np.float32)
        return arr if convert_to_numpy else arr.tolist()

def fixture_search(question,k=3,category=None):
    """실습 흐름을 위한 모의 Top-k (PostgreSQL 미접속)."""
    if type(k) is not int or not (1<=k<=9): raise ValueError('k는 1~9의 정수')
    q=fixture_query(question)
    results=[]
    for row in load_knowledge():
        if category is not None and row['category'] != category: continue
        d=float(1.0 - np.dot(q,doc_vector(row)))
        results.append({**row, 'distance':max(0.0,d), 'source_mode':'simulated'})
    return sorted(results,key=lambda r:(r['distance'],r['id']))[:k]
