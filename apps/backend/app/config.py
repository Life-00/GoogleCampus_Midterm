# --- apps/backend/app/config.py ---

import os
import google.generativeai as genai
from dotenv import load_dotenv
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# 1. .env 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(project_root, '.env')

load_dotenv(dotenv_path=dotenv_path)

print("✅ .env 로드 성공.")

# 2. Gemini 설정
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다.")

genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
print("✅ API 키 및 Gemini 모델 로드 성공.")

# 3. Vertex AI (Imagen) 설정
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1" 
if not GOOGLE_CLOUD_PROJECT:
    raise ValueError("GOOGLE_CLOUD_PROJECT가 .env 파일에 설정되지 않았습니다.")

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=LOCATION)
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
print("✅ Vertex AI (Imagen) 모델 로드 성공.")