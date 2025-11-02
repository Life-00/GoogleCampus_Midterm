# --- apps/backend/app/routes/analysis_routes.py ---

import sys
import os
# ❗️이 파일의 *부모* 폴더(app)를 Python 경로에 추가합니다.
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Blueprint, request, jsonify
# ❗️(수정) 'app' 경로가 추가되었으므로 'services' 패키지에서 임포트합니다.
from services.analysis_service import process_initial_analysis, process_follow_up_chat

# 2. 'analysis_bp' 블루프린트 생성 (이전과 동일)
analysis_bp = Blueprint('analysis_bp', __name__)

# 3. API 엔드포인트 (이전과 동일)
@analysis_bp.route("/analyze", methods=["POST"])
def analyze_endpoint():
    print("ℹ️ /analyze (Blueprint) 요청 받음.")
    if 'image_file' not in request.files:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400
    file = request.files.get('image_file')
    if not file or file.filename == '':
        return jsonify({"error": "파일이 선택되지 않았습니다."}), 400
    try:
        result = process_initial_analysis(file)
        print("✅ 첫 분석 완료, 응답 전송.")
        return jsonify(result)
    except Exception as e:
        print(f"❌ /analyze 오류: {e}")
        return jsonify({"error": f"AI 분석 중 오류 발생: {e}"}), 500

@analysis_bp.route("/chat", methods=["POST"])
def chat_endpoint():
    print("ℹ️ /chat (Blueprint) 요청 받음.")
    data = request.json
    if not data or 'message' not in data or 'history_text' not in data or 'image_base64' not in data:
        return jsonify({"error": "잘못된 요청: message, history_text, image_base64가 필요합니다."}), 400
    try:
        result = process_follow_up_chat(data)
        print("✅ 후속 응답 완료, 응답 전송.")
        return jsonify(result)
    except Exception as e:
        print(f"❌ /chat 오류: {e}")
        return jsonify({"error": f"AI 채팅 중 오류 발생: {e}"}), 500