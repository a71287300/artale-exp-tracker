import cv2
import pytesseract
import re
import numpy as np

# Set Tesseract path - 請根據你的安裝路徑修改
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    """Preprocess image for better OCR accuracy."""
    # 1. 轉灰階
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. CLAHE 對比增強
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    
    # 3. 自適應二值化
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    
    # 4. OTSU 二值化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 5. 膨脹/侵蝕去除雜訊
    kernel = np.ones((2,2), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)
    
    # 6. 去雜訊
    denoised = cv2.fastNlMeansDenoising(binary)
    
    # 7. 銳化
    sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    denoised = cv2.filter2D(denoised, -1, sharpen_kernel)
    
    # 8. 放大
    result = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    return result
def extract_experience(image, show_processed=False, image_placeholder=None, ocr_engine='pytesseract'):
    """Extract experience value from image. 支援 pytesseract 或 easyocr"""
    import streamlit as st
    try:
        processed_image = preprocess_image(image)
        # 顯示處理後的影像（for debug）
        if show_processed:
            if image_placeholder is not None:
                image_placeholder.image(processed_image, caption="處理後影像", channels="GRAY")
            else:
                st.image(processed_image, caption="處理後影像", channels="GRAY")
        text = ''
        if ocr_engine == 'easyocr':
            import easyocr
            reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
            result = reader.readtext(processed_image, detail=0, paragraph=True)
            text = ' '.join(result)
            print(f"Raw OCR text (easyocr): {text}")
        else:
            custom_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789.[]'
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            print(f"Raw OCR text (pytesseract): {text}")
        # 找出所有連續數字，取最長的那一組
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            value = int(max(numbers, key=len))
            print(f"Extracted number: {value}")  # Debug output
            return value
        return None
    except Exception as e:
        print(f"OCR error: {e}")
        return None