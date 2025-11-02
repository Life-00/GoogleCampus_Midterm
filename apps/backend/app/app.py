# --- apps/backend/app/app.py ---

# ⬇️ (핵심) 'sys.path' 관련 코드를 *모두* 삭제 ⬇️
# import sys
# import os
# ... (관련 코드 모두 삭제) ...
# ⬆️ (핵심) ⬆️

from flask import Flask
from flask_cors import CORS
import sys # sys.exit()를 위해 import는 유지

def create_app():
    """Application Factory (앱 공장) 함수"""
    
    app = Flask(__name__)
    CORS(app) 

    # 1. config 임포트
    # 'config.py'는 경로 설정이 필요 없으므로 바로 임포트됩니다.
    try:
        import config
    except ImportError as e:
        print(f"❌ 치명적 오류: config.py 로드 실패. {e}")
        sys.exit(1)

    # 2. 블루프린트 임포트 및 등록
    # 'routes.analysis_routes'가 스스로 경로를 설정할 것입니다.
    try:
        from routes.analysis_routes import analysis_bp
        app.register_blueprint(analysis_bp, url_prefix='/')
        print("✅ 블루프린트('analysis_bp') 등록 성공.")
    except ImportError as e:
        # ❗️이곳에서 오류가 나면 'routes/analysis_routes.py'의 임포트 문제임
        print(f"❌ 치명적 오류: 블루프린트 로드 실패. {e}")
        sys.exit(1)
    
    return app

# 3. 서버 실행
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)