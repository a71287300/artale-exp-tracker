# Artale 經驗值追蹤器

專為 MapleStory Worlds-Artale (繁體中文版) 設計的經驗值追蹤工具，支援即時監控、OCR 辨識與紀錄管理。

---

## 特色功能

- 自動偵測遊戲視窗
- 支援 easyocr / pytesseract 兩種 OCR 引擎
- 使用者自訂擷取區域（獨立儲存於資料庫）
- 即時計算經驗值成長率
- 一鍵儲存練功紀錄（SQLite DB，依使用者分開管理）
- 歷史紀錄瀏覽、刪除
- 暫停/繼續追蹤
- 練功報告自動生成

---

## 安裝需求

- Windows 10/11
- Python 3.10+
- [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)（如需 pytesseract）

### Python 套件
```
streamlit
pytesseract
easyocr
opencv-python
pywin32
numpy
pillow
pygetwindow
pyautogui
```

---

## 安裝步驟

1. 安裝 Tesseract-OCR（如需 pytesseract）  
   下載並安裝 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)  
   預設路徑：`C:\Program Files\Tesseract-OCR`

2. 安裝 Python 依賴
   ```
   pip install -r requirements.txt
   ```

---

## 使用說明

1. 啟動程式
   ```
   streamlit run src/main.py
   ```

2. 登入 Email

3. 設定擷取區域
   - 選擇遊戲視窗
   - 用滑桿調整 X/Y/寬/高
   - 點「瀏覽區域」預覽
   - 點「儲存視窗設定」保存（每位使用者獨立）

4. 開始追蹤
   - 點「開始追蹤」
   - 程式自動計算初始/目前/總獲得/每分鐘經驗值與時間

5. 儲存紀錄
   - 輸入怪物/副本名稱與備註
   - 點「儲存紀錄」

6. 歷史紀錄
   - 登入後可瀏覽、刪除所有紀錄

---

## OCR 引擎切換

- 預設使用 easyocr，辨識率較佳
- 若需切換 pytesseract，請於 `extract_experience` 呼叫時調整 `ocr_engine` 參數

---

## 設定檔說明

### config.json（僅預設值，實際設定依使用者調整並存入資料庫）

```json
{
    "window_region": {
        "x": 53,
        "y": 93,
        "w": 13,
        "h": 3
    }
}
```

---

## 常見問題

- **OCR 無法辨識**
  - 確認 Tesseract-OCR 安裝路徑（如用 pytesseract）
  - 調整擷取區域
  - 遊戲視窗勿被遮蔽或最小化
  - 可切換 easyocr/pytesseract 測試效果

- **視窗擷取失敗**
  - 遊戲視窗需在前景且未最小化
  - 避免全螢幕模式
  - 重新選擇視窗

---

## 授權

MIT（含原作者聲明、來源標註、修改標明）。詳見 [LICENSE](LICENSE)。

---

## 更新紀錄

### v1.1.0
- 支援 easyocr
- 使用者視窗設定與紀錄皆存入資料庫
- 歷史紀錄可瀏覽與刪除

### v1.0.0
- 初始版本
- 基本經驗值追蹤與資料儲存