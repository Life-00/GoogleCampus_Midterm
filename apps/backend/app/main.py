import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
from flask import Flask, request, jsonify
from flask_cors import CORS

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- ⬇️ (신규) Base64 이미지 처리를 위한 라이브러리 ⬇️ ---
import base64
import io
# --- ⬆️ (신규) ⬆️ ---

# --- .env, Flask, 모델 초기화 (이전과 동일) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)
CORS(app) 

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key: raise ValueError("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다.")
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
print("✅ API 키 및 Gemini 모델 로드 성공.")

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1" 
if not GOOGLE_CLOUD_PROJECT: raise ValueError("GOOGLE_CLOUD_PROJECT가 .env 파일에 설정되지 않았습니다.")
vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=LOCATION)
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
print("✅ Vertex AI (Imagen) 모델 로드 성공.")
# --- (초기화 끝) ---


# --- (Imagen 함수 - 이전과 동일) ---
def generate_image_with_imagen(prompt_text):
    print(f"ℹ️ Imagen 호출 (프롬프트: {prompt_text})...")
    try:
        images = imagen_model.generate_images(prompt=prompt_text, number_of_images=1, aspect_ratio="1:1")
        if images and images[0]._image_bytes:
            image_base64 = base64.b64encode(images[0]._image_bytes).decode('utf-8')
            image_data_url = f"data:image/png;base64,{image_base64}"
            print("✅ Imagen 이미지 생성 성공 (Base64 인코딩).")
            return image_data_url
        else: return None
    except Exception as e:
        print(f"❌ Imagen 생성 오류: {e}")
        return None

# --- (파싱 함수 - 이전과 동일) ---
def parse_and_generate_image(gemini_response_text):
    """Gemini 응답 텍스트를 파싱하고, 텍스트와 Imagen 프롬프트를 추출합니다."""
    
    analysis_text = None
    imagen_prompt = None

    # 1. 'ANALYSIS_TEXT' 추출
    match_text = re.search(r'\[ANALYSIS_TEXT_START\]\s*(.*?)\s*\[ANALYSIS_TEXT_END\]', gemini_response_text, re.DOTALL)
    if match_text:
        analysis_text = match_text.group(1).strip()
    
    # 2. 'IMAGEN_PROMPT' 추출
    match_prompt = re.search(r'\[IMAGEN_PROMPT_START\]\s*(.*?)\s*\[IMAGEN_PROMPT_END\]', gemini_response_text, re.DOTALL)
    if match_prompt:
        imagen_prompt = match_prompt.group(1).strip()

    # 3. (오류 방지) 만약 AI가 태그를 빼먹었다면, 그냥 원본 텍스트를 분석글로 사용
    if analysis_text is None:
        analysis_text = gemini_response_text.strip().replace("[IMAGEN_PROMPT_START]", "").replace("[IMAGEN_PROMPT_END]", "")
        print("⚠️ 경고: AI가 [ANALYSIS_TEXT] 태그를 생성하지 않았습니다.")

    print(f"ℹ️ 추출된 분석 텍스트: {analysis_text[:50]}...")
    print(f"ℹ️ 추출된 Imagen 프롬프트: {imagen_prompt}")
    
    image_data_url = None
    if imagen_prompt: # 프롬프트가 성공적으로 추출되었다면
        image_data_url = generate_image_with_imagen(imagen_prompt)
        
    return analysis_text, image_data_url

# --- (시스템 프롬프트 - 이전과 동일) ---
SYSTEM_PROMPT = """
당신은 AI 영양사 '푸드 렌즈'입니다.
당신의 임무는 2가지입니다.

**임무 1: 음식 분석 텍스트 생성**
사용자가 업로드한 음식 사진을 분석하고, 에 나온 것처럼 다음 내용을 포함한 친절하고 훌륭한 분석글을 작성하세요.
- 음식 인식
- 영양 정보 (추정치)
- 건강 팁 (개선할 수 있는 식단 1~2가지 제안 포함)
- 면책 조항 (에서 사용했던 내용)

**임무 2: Imagen 프롬프트 생성**
위 '건강 팁'에서 제안한 *개선된 식단*을 묘사하는,
간단한 영어 이미지 생성 프롬프트를 한 줄 작성하세요. (예: a photorealistic image of a hamburger with a fresh side salad)

**[중요] 출력 형식:**
당신의 최종 응답은 *반드시* 다음 형식을 정확히 따라야 합니다.

[ANALYSIS_TEXT_START]
(여기에 '임무 1'의 분석 텍스트를 모두 작성)
[ANALYSIS_TEXT_END]

[IMAGEN_PROMPT_START]
(여기에 '임무 2'의 영어 프롬프트를 딱 한 줄 작성)
[IMAGEN_PROMPT_END]
"""

# --- ⬇️ (수정) /analyze 엔드포인트: 일회성 호출로 변경 ⬇️ ---
@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    print("ℹ️ /analyze (첫 분석) 요청 받음.")
    
    if 'image_file' not in request.files:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400
    
    file = request.files['image_file']
    if file.filename == '':
        return jsonify({"error": "파일이 선택되지 않았습니다."}), 400

    try:
        img = PIL.Image.open(file)
        
        # 1. start_chat() 대신 generate_content() 사용
        response = gemini_model.generate_content([SYSTEM_PROMPT, img])
        
        # 2. 응답 파싱 및 Imagen 호출
        analysis_text, new_image_url = parse_and_generate_image(response.text)

        # 3. 프론트엔드로 'history' 없이 응답만 전송
        print("✅ 첫 분석 완료, 응답 전송.")
        return jsonify({
            "analysis": analysis_text,
            "new_image_url": new_image_url
            # 'history' 필드 제거
        })

    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        return jsonify({"error": f"AI 분석 중 오류 발생: {e}"}), 500

# --- ⬇️ (수정) /chat 엔드포인트: 이미지와 기록을 모두 받음 ⬇️ ---
@app.route("/chat", methods=["POST"])
def chat_endpoint():
    print("ℹ️ /chat (대화 이어가기) 요청 받음.")
    data = request.json
    
    if not data or 'message' not in data or 'history_text' not in data or 'image_base64' not in data:
        return jsonify({"error": "잘못된 요청: message, history_text, image_base64가 필요합니다."}), 400
        
    user_message = data['message']
    history_text = data['history_text'] # ⭐️ 프론트에서 합친 대화 기록(텍스트)
    image_base64_string = data['image_base64'] # ⭐️ 원본 이미지 (Base64)

    try:
        # 1. Base64 문자열을 다시 PIL 이미지로 변환
        image_data = base64.b64decode(image_base64_string)
        img = PIL.Image.open(io.BytesIO(image_data))
        
        # 2. generate_content에 모든 맥락(이미지, 기록, 새 질문)을 전달
        response = gemini_model.generate_content([
            SYSTEM_PROMPT, # 시스템 역할
            img,           # 원본 이미지
            history_text,  # 이전 대화 (텍스트)
            user_message   # 새 질문
        ])
        
        # 3. 응답 파싱 및 Imagen 호출
        analysis_text, new_image_url = parse_and_generate_image(response.text)
        
        # 4. 프론트엔드로 새 응답 전송
        print("✅ 후속 응답 완료, 응답 전송.")
        return jsonify({
            "analysis": analysis_text,
            "new_image_url": new_image_url
            # 'history' 필드 제거
        })

    except Exception as e:
        print(f"❌ 채팅 중 오류 발생: {e}")
        return jsonify({"error": f"AI 채팅 중 오류 발생: {e}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)