# 遊戲經驗值追蹤器

針對 MapleStory Worlds-Artale (繁體中文版) 設計的經驗值追蹤工具，可即時監控並記錄練功經驗值數據。

## 主要功能

- 自動識別遊戲視窗
- 即時 OCR 經驗值辨識
- 自訂擷取區域位置和大小
- 即時計算經驗值成長率
- 紀錄儲存功能
- 暫停/繼續追蹤
- 自動生成練功報告

## 安裝需求

### 系統需求
- Windows 10/11
- Python 3.8+
- [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)

### Python 套件
```
streamlit         // 使用者介面
pytesseract      // OCR 文字辨識
opencv-python    // 影像處理
pywin32         // Windows API 操作
numpy           // 數值計算
pillow          // 影像處理
```

## 安裝步驟

1. 安裝 Tesseract-OCR:
   - 下載並安裝 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - 預設安裝路徑: `C:\Program Files\Tesseract-OCR`

2. 安裝 Python 依賴:
   ```
   pip install -r requirements.txt
   ```

## 使用說明

1. 啟動程式:
   ```
   python src/main.py
   ```

2. 設定擷取區域:
   - 選擇遊戲視窗
   - 使用滑桿調整 X、Y 位置及寬高
   - 點擊「瀏覽區域」確認擷取範圍
   - 點擊「儲存視窗設定」保存設定

3. 開始追蹤:
   - 點擊「開始追蹤」開始記錄
   - 程式會自動計算:
     - 初始經驗值
     - 目前經驗值
     - 總獲得經驗值
     - 每分鐘平均經驗值
     - 練功時間

4. 儲存紀錄:
   - 輸入練功地點/怪物名稱
   - 可添加額外備註
   - 點擊「儲存紀錄」

## 設定檔說明

### config.json
```json
{
    "window_region": {
        "x": 53,        // X 座標 (百分比)
        "y": 93,        // Y 座標 (百分比)
        "w": 13,        // 寬度 (百分比)
        "h": 3          // 高度 (百分比)
    }
}
```

### record.json
儲存所有練功紀錄，包含:
- 練功地點/怪物
- 備註說明
- 初始/結束經驗值
- 總獲得經驗值
- 平均每分鐘經驗值
- 練功時間

## Streamlit Cloud 部署說明

1. Fork 此專案到你的 GitHub

2. 在 Streamlit Cloud 設定：
   - 連接你的 GitHub 帳號
   - 選擇此專案
   - 設定環境變數：
     - TESSERACT_PATH: Tesseract-OCR 的路徑

3. 資料儲存設定：
   - 資料將儲存在本地 SQLite 資料庫中
   - 每個使用者的紀錄都會分開儲存

4. 使用者認證：
   - 預設提供 demo 帳號
   - 可在管理面板新增使用者

## 疑難排解

1. OCR 無法辨識:
   - 確認 Tesseract-OCR 安裝路徑
   - 調整擷取區域位置
   - 確認遊戲視窗未被遮蔽

2. 視窗擷取失敗:
   - 確認遊戲視窗在前景
   - 檢查遊戲是否全螢幕模式
   - 嘗試重新選擇視窗

## 授權

本專案採用修改版 MIT 授權條款。使用、修改或散布本專案時，必須：
1. 保留原作者版權聲明
2. 標註專案來源
3. 標明修改部分

完整授權條款請參閱 [LICENSE](LICENSE) 文件。

## 更新紀錄

### v1.0.0
- 初始版本發布
- 基本經驗值追蹤功能
- 資料儲存功能