"""환경 확인. Key·Password는 출력하지 않습니다. --live만 GPU/모델/DB 확인."""
from pathlib import Path
import argparse,sys,importlib.util,os
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--live',action='store_true')
    args=parser.parse_args()
    print('Python:',sys.version.split()[0])
    for mod in ['langchain_core','langchain_openai','fastapi','pydantic','pytest',
                'numpy','torch','sentence_transformers','psycopg','pgvector']:
        print(mod, 'installed' if importlib.util.find_spec(mod) else 'MISSING')
    if args.live:
        from coursekit.config import require_cuda,require_setting
        print('CUDA:',require_cuda())
        print('LLM_MODEL:',require_setting('LLM_MODEL'))
        print('OPENAI_API_KEY:', 'configured' if require_setting('OPENAI_API_KEY') else 'missing')
        from coursekit.live import open_db,load_encoder,embedding_contract
        print('E5 contract:',embedding_contract(load_encoder()))
        with open_db() as conn:print('DB:',conn.execute('SELECT 1').fetchone()[0])
if __name__=='__main__':main()
