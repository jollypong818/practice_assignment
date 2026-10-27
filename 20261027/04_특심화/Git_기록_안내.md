# 로컬 Git 이력
이미 저장소가 있으면 재초기화/삭제하지 말고 기존이력을 유지합니다. 새저장소일 때만 프로젝트폴더에서 다음을 실행합니다.
```bash
git init
# 필요시에만 저장소 로컬 사용자 정보를 실제 본인값으로 설정합니다.
git config user.name "Your Name"
git config user.email "you@example.com"
git status
git add README.md .gitignore main.py preprocessing.py evaluate.py checks.py model_config.py course_support.py requirements-lock.txt data reports
git diff --cached --stat
git commit -m "Add Day7 ensemble experiment"
```
그다음 보고서/테스트 수정 후 해당파일만 add/commit합니다. `git log --oneline -5`와 `git status --short`를 실행증거에 남깁니다.
`.venv`, 비밀키, 모델joblib은 추가하지 않습니다. `git add .`를 무심코 실행하지 않습니다.
원격push·계정·네트워크는 필수조건이 아닙니다. 현재 폴더상태/검토대상부터 확인합니다.
