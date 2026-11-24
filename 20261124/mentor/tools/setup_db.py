"""Day27 전용 d27_ Schema 준비. --apply 없이는 DB·E5를 실행하지 않습니다."""
from pathlib import Path
import sys,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    if not args.apply:
        print('실제 준비: python tools/setup_db.py --apply')
        print('RAG_SCHEMA=d27_rag / pgvector 확장 확인 / CUDA GPU 필수')
        return 0
    from coursekit.io import load_json,save_report
    from coursekit.live import open_db,load_encoder,embedding_contract,encode
    from coursekit.db import publish
    from coursekit.config import schema_name
    corpus=load_json('corpus.json')
    encoder=load_encoder();contract=embedding_contract(encoder)
    vectors=[encode(encoder,item['body'],'passage: ') for item in corpus]
    with open_db() as conn:
        with conn.transaction():
            sources=publish(conn,corpus,vectors,contract)
    save_report(ROOT/'tools','setup_result.json',{'schema':schema_name(),
        'mode':'live_e5_cuda_postgresql','contract':contract,'sources':sources})
    print('Day27 데이터 준비 완료',len(sources))
    return 0
if __name__=='__main__':raise SystemExit(main())
