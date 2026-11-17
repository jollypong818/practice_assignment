"""통합본에서 TODO 정답 대응을 검사합니다. 파일 수정과 API 호출은 하지 않습니다."""
from pathlib import Path
import argparse
import ast
import re

BLOCK = re.compile(r'(?P<start>^[ \t]*# BEGIN (?P<id>D22-[A-Z0-9-]+)\n)(?P<body>.*?)(?P<end>^[ \t]*# END (?P=id))', re.M | re.S)


def main():
    mentor = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mentee', type=Path, default=mentor.parent / 'mentee')
    args = parser.parse_args()
    if not args.mentee.is_dir():
        parser.error('통합본의 mentee 경로가 필요합니다. --mentee로 지정하세요.')
    total = 0
    for level in ['01_basic', '02_intermediate', '03_advanced']:
        count = 0
        for teacher in sorted((mentor / level).rglob('*.py')):
            source = teacher.read_text(encoding='utf-8')
            answers = {m['id']: m['body'] for m in BLOCK.finditer(source)}
            if not answers:
                continue
            student = args.mentee / teacher.relative_to(mentor)
            text = student.read_text(encoding='utf-8')
            found = {m['id'] for m in BLOCK.finditer(text)}
            if found != set(answers):
                raise AssertionError(f'TODO ID 불일치: {student}')
            restored = BLOCK.sub(lambda m: m['start'] + answers[m['id']] + m['end'], text)
            if ast.dump(ast.parse(restored)) != ast.dump(ast.parse(source)):
                raise AssertionError(f'정답 대입 후 코드 구조 불일치: {student}')
            count += len(answers)
        total += count
        print(f'{level}: {count}개 TODO 정답 대응 확인')
    print(f'총 {total}개 확인. 원본 변경·API 전송 없음.')


if __name__ == '__main__':
    main()
