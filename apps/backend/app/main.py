
import os
import re # 1. Gemini 응답을 파싱하기 위해 're' (정규표현식) 임포트
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- ⬇️ Vertex AI (Imagen) 라이브러리 임포트 ⬇️ ---
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
# --- ⬆️ Vertex AI (Imagen) 라이브러리 임포트 ⬆️ ---


# --- .env 파일 경로 설정 (이전과 동일) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(project_root, '.env')

load_dotenv(dotenv_path=dotenv_path)

# --- Flask 앱 설정 (이전과 동일) ---
app = Flask(__name__)
CORS(app) 

# --- ⬇️ API 키 및 모델 초기화 ⬇️ ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(f"GOOGLE_API_KEY를 찾을 수 없습니다. {dotenv_path} 파일을 확인하세요.")

# 1. Gemini 설정 (이전과 동일)
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
print("✅ API 키 및 Gemini 모델 로드 성공.")

# 2. Vertex AI (Imagen) 설정
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT") # .env 파일에 프로젝트 ID가 있어야 함
LOCATION = "us-central1" # 또는 본인의 리전

if not GOOGLE_CLOUD_PROJECT:
    raise ValueError("GOOGLE_CLOUD_PROJECT가 .env 파일에 설정되지 않았습니다.")

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=LOCATION)
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002") #
print("✅ Vertex AI (Imagen) 모델 로드 성공.")
# --- ⬆️ API 키 및 모델 초기화 ⬆️ ---


def generate_image_with_imagen(prompt_text):
    """Imagen을 호출하여 이미지를 생성하고 URL을 반환합니다."""
    print(f"ℹ️ Imagen 호출 (프롬프트: {prompt_text})...")
    try:
        #
        images = imagen_model.generate_images(
            prompt=prompt_text,
            number_of_images=1,
            aspect_ratio="1:1" #
        )
        # 생성된 이미지의 GCS URL이나 바이트를 얻어야 하지만, 
        # 여기서는 간단히 로컬에 저장하고 서빙하는 대신, 
        # (주의: generate_images는 URL을 직접 반환하지 않습니다. 
        # 실제로는 이미지를 GCS에 저장하고 URL을 생성해야 하지만,
        # 데모를 위해 임시 파일로 저장하고 Base64로 인코딩하는 것이 더 빠를 수 있습니다.
        # 우선은 ._image_bytes를 사용해봅니다.)
        
        if images and images[0]._image_bytes:
            # 이미지를 Base64로 인코딩하여 프론트엔드로 바로 전송
            import base64
            image_base64 = base64.b64encode(images[0]._image_bytes).decode('utf-8')
            image_data_url = f"data:image/png;base64,{image_base64}"
            print("✅ Imagen 이미지 생성 성공 (Base64 인코딩).")
            return image_data_url
        else:
            return None
            
    except Exception as e:
        print(f"❌ Imagen 생성 오류: {e}")
        return None


def analyze_image_with_gemini(image_file):
    """Gemini AI에게 프롬프트와 이미지를 보내 분석을 요청하는 함수"""
    
    img = PIL.Image.open(image_file)
    
    # 3. --- ⬇️ Gemini 프롬프트 고도화 ⬇️ ---
    system_prompt = """
    당신은 AI 영양사 '푸드 렌즈'입니다.
    당신의 임무는 사용자가 업로드한 음식 사진을 분석하고, 
    일반인이 이해하기 쉬운 건강 정보를 제공하는 것입니다.

    다음 단계를 *반드시* 순서대로 따르세요:
    
    1.  **음식 인식:** 사진 속의 주요 음식들을 인식합니다.
    2.  **영양 정보 (추정):** 인식된 음식을 기반으로 '총 칼로리'와 '총 단백질'을 *대략적으로* 추정합니다.
    3.  **건강 팁:** 해당 식단에 대해 간단한 건강 팁 1~2가지를 제공합니다. (예: "여기에 샐러드를 곁들이면 좋습니다.")
    4.  **면책 조항:** 마지막에 "본 정보는 AI의 추정치이며..." 문구를 *반드시* 포함하세요.
    
    출력: 분석 결과를 친절하고 간결한 문장으로 설명해주세요.
    
    ---
    
    **[IMAGEN_PROMPT_START]**
    (위 '건강 팁'을 바탕으로, 개선된 식단의 모습을 묘사하는 *간단한 영어* 이미지 생성 프롬프트를 딱 한 줄로 작성하세요. 
    예: a photorealistic image of a hamburger with a fresh side salad on a wooden table)
    **[IMAGEN_PROMPT_END]**
    """
    
    prompt_package = [system_prompt, img]
    response = gemini_model.generate_content(prompt_package)
    
    return response.text
    # 4. --- ⬆️ Gemini 프롬프트 고도화 ⬆️ ---


@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    print("ℹ️ /analyze 요청 받음.")
    
    if 'image_file' not in request.files:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400
    
    file = request.files['image_file']
    
    if file.filename == '':
        return jsonify({"error": "파일이 선택되지 않았습니다."}), 400

    try:
        # 5. Gemini 분석 호출
        gemini_raw_response = analyze_image_with_gemini(file)
        
        # 6. --- ⬇️ Gemini 응답 파싱 ⬇️ ---
        analysis_text = gemini_raw_response
        imagen_prompt = None
        
        # 정규표현식으로 IMAGEN_PROMPT_START와 END 사이의 텍스트 추출
        match = re.search(r'\[IMAGEN_PROMPT_START\]\s*(.*?)\s*\[IMAGEN_PROMPT_END\]', gemini_raw_response, re.DOTALL)
        if match:
            imagen_prompt = match.group(1).strip()
            # 프론트에 보낼 텍스트에서 프롬프트 부분은 제거
            analysis_text = re.sub(r'\[IMAGEN_PROMPT_START\].*?\[IMAGEN_PROMPT_END\]', '', gemini_raw_response, flags=re.DOTALL).strip()
        
        print(f"✅ Gemini 분석 완료.")
        print(f"ℹ️ 추출된 Imagen 프롬프트: {imagen_prompt}")
        # 6. --- ⬆️ Gemini 응답 파싱 ⬆️ ---

        image_data_url = None
        if imagen_prompt:
            # 7. Imagen 호출
            image_data_url = generate_image_with_imagen(imagen_prompt)
        
        # 8. 프론트엔드로 두 AI의 결과 전송
        return jsonify({
            "analysis": analysis_text,
            "new_image_url": image_data_url # Imagen이 생성한 Base64 이미지 URL
        })

    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        return jsonify({"error": f"AI 분석 중 오류 발생: {e}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)