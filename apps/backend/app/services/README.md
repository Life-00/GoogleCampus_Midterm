# ⚙️ Services (Business Logic)

이 폴더는 애플리케이션의 **서비스 레이어(Service Layer)**로서, 모든 실제 비즈니스 로직을 담당합니다.

## 🎯 핵심 역할

* `routes` 레이어로부터 요청을 받아, **실제 작업**을 수행합니다.
* `Gemini` API를 호출하여 텍스트 분석을 수행합니다.
* [cite_start]`Imagen` (Vertex AI) API를 호출하여 이미지를 생성합니다. [cite: 56]
* AI의 응답 텍스트를 파싱하고(`[ANALYSIS_TEXT_START]` 등) 데이터를 가공합니다.
* `prompts.py`에서 시스템 프롬프트를, `config.py`에서 초기화된 AI 모델을 가져와 사용합니다.

`routes`나 `app.py`가 "어떻게" 작동하는지 알 필요 없이, 오직 "무엇을" 할지만 정의하는 파일들이 모여있습니다.
