import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image  

# --- .env 파일 경로 설정 (이전과 동일) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(project_root, '.env')

# --- .env 파일 로드 (이전과 동일) ---
load_dotenv(dotenv_path=dotenv_path)

# --- ⬇️ 여기가 중요: 핵심 프롬프트 ⬇️ ---
def build_prompt(image):
    """AI에게 보낼 프롬프트와 이미지를 조합합니다."""
    
    # 1. AI에게 부여할 역할과 지시사항 (시스템 프롬프트)
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
    
    # 2. 모델에게 보낼 최종 입력물 조합
    # 텍스트(지시사항)와 이미지(분석 대상)를 리스트로 전달합니다.
    return [system_prompt, image]


def main():
    # --- API 키 불러오기 (이전과 동일) ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(f"GOOGLE_API_KEY를 찾을 수 없습니다. {dotenv_path} 파일을 확인하세요.")
    print("API 키 로드 성공.")

    # --- API 설정 (이전과 동일) ---
    genai.configure(api_key=api_key)
    
    # --- 모델 설정 (이전과 동일) ---
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    # --- 'test_food.jpg' 이미지 파일 열기 (이전과 동일) ---
    img_path = os.path.join(current_dir, 'test_food.jpg')
    
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"{img_path} 파일을 찾을 수 없습니다. main.py와 같은 폴더에 넣어주세요.")
        
    img = PIL.Image.open(img_path)
    print(f"{img_path} 이미지 파일 로드 성공.")
    
    # --- ⬇️ 여기가 수정된 부분 ⬇️ ---
    
    # 4. AI에게 '새로운 프롬프트'와 '이미지'를 함께 전송
    print("Gemini Vision 모델에 '푸드 렌즈' 프롬프트를 전송합니다...")
    
    # 38번 답변 [cite: 38]의 단순 프롬프트 대신, 우리가 새로 정의한 build_prompt 함수 사용
    prompt_package = build_prompt(img)
    
    response = model.generate_content(prompt_package)
    
    # 5. 모델의 응답 출력
    print("\n--- '푸드 렌즈' AI 응답 ---")
    print(response.text)
    print("----------------------------")

if __name__ == "__main__":
    main()