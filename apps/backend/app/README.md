🚀 프로젝트 실행 방법 (최종)
이 프로젝트는 **백엔드(Flask)**와 **프론트엔드(HTML/JS)**가 분리되어 있어, 터미널 2개를 동시에 실행해야 합니다.

[ 1번 터미널: 백엔드 (API 서버) ]
### 1. Poetry 가상 환경을 활성화합니다.
```Bash
poetry shell
```

### 2. 백엔드 app.py 파일이 있는 폴더로 이동합니다.
```
Bash
cd apps/backend/app
```

### 3. Flask 서버를 실행합니다. (main.py가 아닌 app.py입니다.)
```
Bash
python app.py
* Running on http://127.0.0.1:5000 메시지가 뜨고 멈춰있으면 성공입니다. (이 창을 끄지 마세요.)
```
