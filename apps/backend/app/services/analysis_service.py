# --- apps/backend/app/services/analysis_service.py ---

import sys
import os
# ❗️이 파일의 *부모* 폴더(app)를 Python 경로에 추가합니다.
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import re
import base64
import io
import PIL.Image

# 'config'와 'prompts'를 이제 찾을 수 있습니다.
from config import gemini_model, imagen_model
from prompts import SYSTEM_PROMPT 

# --- (Imagen 함수 - 변경 없음) ---
def _generate_image_with_imagen(prompt_text):
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

# --- (파싱 함수 - 변경 없음) ---
def _parse_and_generate_image(gemini_response_text):
    analysis_text = None
    imagen_prompt = None
    match_text = re.search(r'\[ANALYSIS_TEXT_START\]\s*(.*?)\s*\[ANALYSIS_TEXT_END\]', gemini_response_text, re.DOTALL)
    if match_text:
        analysis_text = match_text.group(1).strip()
    match_prompt = re.search(r'\[IMAGEN_PROMPT_START\]\s*(.*?)\s*\[IMAGEN_PROMPT_END\]', gemini_response_text, re.DOTALL)
    if match_prompt:
        imagen_prompt = match_prompt.group(1).strip()
    if analysis_text is None:
        analysis_text = gemini_response_text.strip().replace("[IMAGEN_PROMPT_START]", "").replace("[IMAGEN_PROMPT_END]", "")
        print("⚠️ 경고: AI가 [ANALYSIS_TEXT] 태그를 생성하지 않았습니다.")
    print(f"ℹ️ 추출된 분석 텍스트: {analysis_text[:50]}...")
    print(f"ℹ️ 추출된 Imagen 프롬프트: {imagen_prompt}")
    image_data_url = None
    if imagen_prompt:
        image_data_url = _generate_image_with_imagen(imagen_prompt)
    return analysis_text, image_data_url

# --- (공용 함수들 - 변경 없음) ---
def process_initial_analysis(image_file):
    img = PIL.Image.open(image_file)
    response = gemini_model.generate_content([SYSTEM_PROMPT, img])
    analysis_text, new_image_url = _parse_and_generate_image(response.text)
    return {"analysis": analysis_text, "new_image_url": new_image_url}

def process_follow_up_chat(chat_data):
    user_message = chat_data['message']
    history_text = chat_data['history_text']
    image_base64_string = chat_data['image_base64']
    image_data = base64.b64decode(image_base64_string)
    img = PIL.Image.open(io.BytesIO(image_data))
    response = gemini_model.generate_content([
        SYSTEM_PROMPT,
        img,
        history_text,
        user_message
    ])
    analysis_text, new_image_url = _parse_and_generate_image(response.text)
    return {"analysis": analysis_text, "new_image_url": new_image_url}