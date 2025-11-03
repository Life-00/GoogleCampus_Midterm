
## 🐍 Poetry (Python) 환경 설정 가이드

이 프로젝트는 `Poetry`를 사용하여 Python 가상 환경과 라이브러리(의존성)를 관리합니다.

## 🛠️ (필수) 로컬 개발 환경 설정

이 데모는 2개의 Google AI API와 Google Cloud 인증을 사용합니다.

### 0. .env 파일 설정

프로젝트 최상위 폴더 (`/`)에 `.env` 파일을 생성하고 다음 2가지 키를 입력해야 합니다.

```dotenv
# Gemini API 키 (Google AI Studio에서 발급)
GOOGLE_API_KEY="..."

# Imagen API를 위한 Google Cloud 프로젝트 ID
GOOGLE_CLOUD_PROJECT="..."
```

### 1. (필수) 개발 환경 활성화

코드를 작성하거나 실행하기 전, **매번** 터미널에서 **가장 먼저** 다음 명령어를 실행하여 Poetry 가상 환경을 활성화해야 합니다.

```bash
poetry shell
```

성공적으로 실행되면 터미널 프롬프트(명령줄) 맨 앞에 (googlecampus_midterm-py3.10)과 같이 현재 프로젝트의 가상 환경 이름이 표시됩니다.

이후 모든 python 또는 poetry 관련 명령어는 이 활성화된 셸 안에서 실행해야 합니다.

### 2. 📦 새 라이브러리(패키지) 설치
pip install을 직접 사용하지 않습니다. 대신 poetry add를 사용합니다.

```bash
# 예시: pandas 라이브러리를 설치하는 경우
poetry add pandas
```

이 명령어를 사용하면 pyproject.toml 파일에 해당 라이브러리가 자동으로 기록되고, poetry.lock 파일이 업데이트되며, 가상 환경에 실제 패키지가 설치됩니다.

### 3. ▶️ Python 스크립트 실행
환경이 활성화된 상태(poetry shell 실행 후)에서 평소처럼 python 명령어로 스크립트 파일을 실행합니다.

```bash
# 예시: main.py 파일을 실행하는 경우
python main.py
```

### 4. 📁 (참고) 주요 파일 설명
pyproject.toml: 이 프로젝트의 핵심 설정 파일입니다. requirements.txt의 역할을 대체하며, 프로젝트의 기본 정보와 필요한 라이브러리 목록(의존성)이 모두 여기에 기록됩니다.

poetry.lock: pyproject.toml을 기반으로 설치된 라이브러리들의 정확한 버전을 기록하는 파일입니다. 이 파일 덕분에 다른 환경에서도 항상 동일한 버전의 라이브러리를 설치할 수 있습니다. (직접 수정하지 마세요.)

.venv/: Poetry가 생성한 Python 가상 환경 폴더입니다. (.gitignore에 추가되어 Git이 무시합니다.)

.env: API 키와 같은 비밀 정보를 저장하는 파일입니다. (.gitignore에 추가되어 Git이 절대 무시합니다.)

### 5. (참고) 환경 비활성화
가상 환경에서 나오고 싶다면, 활성화된 셸에서 exit를 입력합니다.

```bash
exit
```
