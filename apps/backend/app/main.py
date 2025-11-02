
import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
from flask import Flask, request, jsonify
from flask_cors import CORS # 1. CORS 임포트

# --- .env 파일 경로 설정 (이전과 동일) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(project_root, '.env')

# --- .env 파일 로드 (이전과 동일) ---
load_dotenv(dotenv_path=dotenv_path)

# --- ⬇️ Flask 앱 설정 ⬇️ ---
app = Flask(__name__)
# 2. CORS 설정: 모든 주소(*)에서 오는 요청을 허용합니다.
CORS(app) 
# --- ⬆️ Flask 앱 설정 ⬆️ ---

# --- API 키 로드 및 Gemini 설정 (main 함수 밖으로 이동) ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(f"GOOGLE_API_KEY를 찾을 수 없습니다. {dotenv_path} 파일을 확인하세요.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
print("✅ API 키 및 Gemini 모델 로드 성공.")

def analyze_image_with_gemini(image_file):
    """Gemini AI에게 프롬프트와 이미지를 보내 분석을 요청하는 함수"""
    
    img = PIL.Image.open(image_file) # 3. 파일로 바로 이미지 열기
    
    system_prompt = """
    당신은 AI 영양사 '푸드 렌즈'입니다. 
    당신의 임무는 사용자가 업로드한 음식 사진을 분석하고, 
    일반인이 이해하기 쉬운 건강 정보를 제공하는 것입니다.


    다음 단계를 *반드시* 순서대로 따르세요:
    
    1.  음식 인식: 사진 속의 주요 음식들을 인식합니다.
    2.  영양 정보 (추정): 인식된 음식을 기반으로 '총 칼로리'와 '총 단백질'을 *대략적으로* 추정합니다.  (이것은 추정치임을 명시하세요)
    3.  건강 팁: 해당 식단에 대해 일반인이 실천할 수 있는 간단한 건강 팁 1~2가지를 제공합니다.  (예: "단백질이 풍부하네요!", "섬유질을 보충하면 좋습니다.")
    
    출력: 분석 결과를 친절하고 간결한 문장으로 설명해주세요.
    """
    
    prompt_package = [system_prompt, img]
    response = model.generate_content(prompt_package)
    
    return response.text

# --- ⬇️ API 엔드포인트 ⬇️ ---
@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    """/analyze 주소로 POST 요청이 오면 실행되는 함수"""
    
    print("ℹ️ /analyze 요청 받음.")
    
    # 4. 프론트엔드에서 'image_file'이라는 이름으로 보낸 파일 받기
    if 'image_file' not in request.files:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400
    
    file = request.files['image_file']
    
    if file.filename == '':
        return jsonify({"error": "파일이 선택되지 않았습니다."}), 400

    try:
        # 5. AI 분석 함수 호출
        analysis_result = analyze_image_with_gemini(file)
        
        # 6. 프론트엔드로 JSON 형태로 결과 전송
        print("✅ 분석 완료, 결과 전송.")
        return jsonify({"analysis": analysis_result})

    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        return jsonify({"error": f"AI 분석 중 오류 발생: {e}"}), 500
# --- ⬆️ API 엔드포인트 ⬆️ ---


# 7. 스크립트가 직접 실행될 때 Flask 서버를 5000번 포트로 실행
if __name__ == "__main__":
    # host='0.0.0.0'은 모든 IP에서 접근 가능하게 함
    app.run(host='0.0.0.0', port=5000, debug=True)