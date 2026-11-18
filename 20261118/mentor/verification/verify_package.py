"""Day23 로컬 패키지의 재현 가능한 정적/모의 검수.

실제 모델 다운로드, Windows nmake, PostgreSQL DB에 연결하지 않습니다.
강사용 단독 배포에서도 실행할 수 있으며, mentee가 함께 있으면 TODO 장벽도 검사.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import subprocess, sys, json, hashlib

MENTOR=Path(__file__).resolve().parents[1]
ROOT=MENTOR.parent
STUDENT=ROOT/'mentee'
LEVELS={'01_basic':3,'02_intermediate':5,'03_advanced':6}

def exercise_paths(root):
    return sorted(root.glob('0[1-3]_*/0[1-8]_*/main.py'))

def verify():
    entries=exercise_paths(MENTOR)
    assert len(entries)==24,(len(entries),'강사용 main.py가 24개인지 확인')
    checks=Counter()
    rows=[]
    for entry in entries:
        result=subprocess.run([sys.executable,str(entry),'--mode','fixture'],capture_output=True,text=True,timeout=40)
        if result.returncode!=0:raise RuntimeError('강사용 실패: '+str(entry)+'\n'+result.stderr[-4000:])
        relative=entry.relative_to(MENTOR)
        output=json.loads((entry.parent/'outputs'/('exercise_'+entry.parent.name[:2]+'.json')).read_text(encoding='utf-8'))
        assert output['exercise']==int(entry.parent.name[:2])
        assert output['source_mode'] not in ('e5_live','pgvector_live','pgvector_exact')
        rows.append({'entry':str(relative),'result':'passed','source_mode':output['source_mode']})
        checks['mentor_fixture_passed']+=1
    if STUDENT.exists():
        student_entries=exercise_paths(STUDENT)
        assert len(student_entries)==24,len(student_entries)
        for entry in student_entries:
            result=subprocess.run([sys.executable,str(entry),'--mode','fixture'],capture_output=True,text=True,timeout=20)
            if result.returncode==0 or 'NotImplementedError' not in result.stderr:
                raise AssertionError('수강생용 TODO 장벽 오류: '+str(entry)+'\n'+result.stderr[-600:])
            checks['mentee_todo_blocked']+=1
    for side,root in [('mentor',MENTOR),('mentee',STUDENT)]:
        if not root.exists():continue
        for level,count in LEVELS.items():
            starts=sum(p.read_text(encoding='utf-8').count('# BEGIN D23-') for p in (root/level).rglob('*.py'))
            assert starts==count*8,(side,level,starts)
            checks[side+'_todo_total']+=starts
    for x in MENTOR.rglob('*.py'):
        compile(x.read_text(encoding='utf-8'),str(x),'exec')
        checks['mentor_files_compiled']+=1
    for x in STUDENT.rglob('*.py') if STUDENT.exists() else []:
        compile(x.read_text(encoding='utf-8'),str(x),'exec')
        checks['mentee_files_compiled']+=1
    # 실습 파일은 정확한 지식 스냅샷을 내장합니다. 검사 기준 SHA는 배포 시점에 별도 기록.
    sys.path.insert(0,str(MENTOR/'common'))
    from day23kit.data import load_knowledge
    raw=json.dumps(load_knowledge(),sort_keys=True,ensure_ascii=False,separators=(',',':'))
    sha=hashlib.sha256(raw.encode('utf-8')).hexdigest()
    assert sha==(MENTOR/'verification/HTML_KNOWLEDGE_SHA256.txt').read_text().strip()
    checks['html_knowledge_snapshot_match']+=1
    if STUDENT.exists():
        assert (STUDENT/'common/data/knowledge_search_v2.json').read_bytes()==(MENTOR/'common/data/knowledge_search_v2.json').read_bytes()
        checks['both_sides_same_knowledge_bytes']+=1
    report={'reference':'Day23 HTML 80 scenes, 8 practices',
            'runtime':'offline fixture, Python '+sys.version.split()[0],
            'checks':dict(checks),'total_verified_exercise_runs':checks['mentor_fixture_passed'],
            'real_pgvector_build_tested':False,'real_e5_tested':False,
            'student_todo_exercises_blocked':checks['mentee_todo_blocked'],
            'knowledge_sha256':sha,'details':rows}
    (MENTOR/'verification/REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':verify()
