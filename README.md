# GoogleCampus_Midterm
GoogleCampus_Midterm_Homework


# 🚀 구글 AI 미니 프로젝트 Git 사용 가이드
이 문서는 프로젝트의 Git 워크플로우와 코드 관리 규칙을 정의합니다.

## 1. 핵심 브랜치 전략

이 프로젝트는 두 종류의 브랜치를 사용합니다.

* **`main` 브랜치:**
    * 항상 **오류 없이 실행되는** 안정적인 최종본(버전)이 위치하는 곳입니다.
    * 이 브랜치에 직접 코드를 수정하거나 커밋(commit)하지 않습니다.

* **`feature` 브랜치:**
    * 새로운 기능 개발, 버그 수정 등 모든 실제 작업은 이 브랜치에서 이루어집니다.
    * 브랜치 이름은 `feature/기능요약` 형식을 따릅니다. (예: `feature/gemini-api-setup`, `feature/web-ui`)
    * 작업이 완료되면 `main` 브랜치로 병합(Merge)합니다.

## 2. 기본 작업 흐름 (Workflow)

새로운 기능(예: 'Gemini API 연동')을 추가할 때의 흐름입니다.


### 1단계: (시작 전) `main` 브랜치 최신화

```bash
# 1. main 브랜치로 이동
git checkout main

# 2. GitHub 저장소의 최신 코드를 로컬로 가져오기
git pull origin main
```

### 2단계: 새 feature 브랜치 생성

```bash
# 3. 'feature/기능이름'으로 새 브랜치를 만들고 이동
git checkout -b feature/gemini-api-call
```

### 3단계: 코드 작업 및 저장 (Commit)
여기서 poetry shell로 활성화된 가상 환경에서 코드를 작성하고 테스트합니다.

```bash
# 4. (열심히 코딩...)

# 5. 작업한 모든 파일을 저장 목록에 추가
git add .

# 6. 작업 내역을 메시지와 함께 로컬 저장소에 저장 (커밋)
git commit -m "feat: Gemini API 호출 함수 기본 골격 추가"

Tip! 작업은 기능 단위로 잘게 쪼개서 add와 commit을 자주 하는 것이 좋습니다.
```


### 4단계: main 브랜치에 병합하기
기능이 완성되면, feature 브랜치의 내용을 main으로 합칩니다.

```bash
# 7. main 브랜치로 복귀
git checkout main

# 8. 방금 작업한 'feature/gemini-api-call' 브랜치를 main으로 병합
git merge feature/gemini-api-call
```

### 5단계: GitHub에 업로드
로컬 main 브랜치에 합쳐진 최종본을 GitHub 원격 저장소에 업로드합니다.

```bash
# 9. GitHub(origin)으로 main 브랜치의 변경 사항을 업로드
git push origin main
```

### 6단계: (선택) 브랜치 정리

```bash
# 10. 작업이 끝난 feature 브랜치 삭제
git branch -d feature/gemini-api-call
```


## 3. ✍️ 커밋 메시지 규칙
커밋 메시지는 "무엇을" 했는지 명확하게 알 수 있도록 타입 태그를 붙이는 것을 권장합니다. (이는 과제 평가의 '코드 이해도' 항목에도 긍정적인 영향을 줄 수 있습니다.)

feat: : 새로운 기능 추가

fix: : 버그 수정

docs: : README.md 등 문서 수정

style: : 코드 포맷팅, 세미콜론 누락 등 (기능 변경 없음)

refactor: : 코드 리팩토링

chore: : 빌드 설정, 라이브러리 추가 등 기타 작업

좋은 예:

feat: Gemini API 호출 함수 추가

fix: API 키 로드 시 발생하는 오류 수정

docs: Git 워크플로우 가이드라인 추가

나쁜 예:

수정

버그 고침

커밋


## 추가

만약 main에 합치기 전에, 작업 중인 feature 브랜치 자체를 GitHub에 올려서 백업하거나 다른 사람에게 보여주고 싶다면, push할 때 그 브랜치 이름을 명시해야 합니다.

예를 들어 feature/gemini-api-call 브랜치에서 작업 중일 때,

```bash

# 1. (현재 브랜치 확인)
git checkout feature/gemini-api-call

# 2. 이 브랜치를 'origin'(GitHub)에 똑같은 이름으로 업로드
# -u 옵션은 한 번만 쓰면 됨 (로컬 브랜치와 원격 브랜치를 '연결'해줌)
git push -u origin feature/gemini-api-call
이렇게 push를 해야 비로소 GitHub 웹사이트에 feature/gemini-api-call 브랜치가 보이게 됩니다.
```
