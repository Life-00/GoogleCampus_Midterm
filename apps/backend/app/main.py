import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- 여기가 중요 ---
# 1. 현재 main.py 파일의 절대 경로를 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. main.py가 'app' -> 'backend' -> 'apps' 안에 있으므로, 
#    세 단계(.env 파일이 있는) 상위 폴더로 이동합니다.
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

# 3. .env 파일의 최종 경로를 계산합니다.
dotenv_path = os.path.join(project_root, '.env')

# --- ⬇️ 디버깅 코드 추가 ⬇️ ---
print(f"1. .env 파일 경로: {dotenv_path}")
print(f"2. 해당 경로에 .env 파일이 존재하나요? {os.path.exists(dotenv_path)}")
# --- ⬆️ 디버깅 코드 추가 ⬆️ ---

# 4. load_dotenv()에 .env 파일 경로를 명시적으로 알려줍니다.
load_dotenv(dotenv_path=dotenv_path)


def main():
    # 5. .env 파일에서 "GOOGLE_API_KEY" 값을 가져옵니다.
    api_key = os.getenv("GOOGLE_API_KEY")

    # --- ⬇️ 디버깅 코드 추가 ⬇️ ---
    print(f"3. 불러온 API 키 (앞 5자리): {str(api_key)[:5]}...")
    # --- ⬆️ 디버깅 코드 추가 ⬆️ ---
    
    # 6. 키가 제대로 불러와졌는지 확인합니다.
    if not api_key:
        raise ValueError("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다. (파일 경로와 변수명을 확인하세요)")

    print("API 키 로드 성공.")

    # 7. Google AI (Gemini) API 설정을 완료합니다.
    genai.configure(api_key=api_key)
    
    # 8. 사용할 모델을 초기화합니다. (gemini-pro -> gemini-1.5-flash로 변경)
    model = genai.GenerativeModel('gemini-2.5-flash') # gemini-pro보다 최신이고 빠른 모델로 변경했습니다.
    
    # 9. 모델에게 간단한 테스트 메시지를 보냅니다.
    print("Gemini 모델에 테스트 프롬프트를 전송합니다...")
    response = model.generate_content("Hello, world!")
    
    # 10. 모델의 응답을 출력합니다.
    print("\n--- 모델 응답 ---")
    print(response.text)
    print("-----------------")

# 이 스크립트가 직접 실행될 때 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()