import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image  # 1. 이미지 처리 라이브러리 불러오기

# --- .env 파일 경로 설정 (이전과 동일) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(project_root, '.env')

# --- .env 파일 로드 (이전과 동일) ---
load_dotenv(dotenv_path=dotenv_path)

def main():
    # --- API 키 불러오기 (이전과 동일) ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(f"GOOGLE_API_KEY를 찾을 수 없습니다. {dotenv_path} 파일을 확인하세요.")
    print("API 키 로드 성공.")

    # --- API 설정 (이전과 동일) ---
    genai.configure(api_key=api_key)
    
    # --- ⬇️ 여기가 중요 ⬇️ ---

    # 2. 모델 이름을 'gemini-pro-vision' (비전 모델)으로 변경
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 3. 'test_food.jpg' 이미지 파일 열기
    # (main.py와 같은 폴더에 파일이 있다고 가정)
    img_path = os.path.join(current_dir, 'test_food.jpg')
    
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"{img_path} 파일을 찾을 수 없습니다. main.py와 같은 폴더에 넣어주세요.")
        
    img = PIL.Image.open(img_path)
    
    print(f"{img_path} 이미지 파일 로드 성공.")
    
    # 4. AI에게 '텍스트 프롬프트'와 '이미지'를 함께 전송
    print("Gemini Vision 모델에 이미지와 프롬프트를 전송합니다...")
    
    prompt = "이 사진에 있는 음식은 무엇인가요? 간단하게만 답해주세요."
    
    # model.generate_content는 [텍스트, 이미지, 텍스트, 이미지...] 순서로 리스트를 받음
    response = model.generate_content([prompt, img])
    
    # 5. 모델의 응답 출력
    print("\n--- 모델 응답 ---")
    print(response.text)
    print("-----------------")

if __name__ == "__main__":
    main()