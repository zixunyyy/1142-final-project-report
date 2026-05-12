# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (輸入心情) | GET | `/` | `index.html` | 顯示首頁與文字輸入表單 |
| 送出情緒分析 | POST | `/analyze` | `result.html` | 接收使用者輸入，執行情緒分析並回傳建議結果 |
| 歷史紀錄儀表板 | GET | `/dashboard` | `dashboard.html` | 顯示圖表統計與過去所有的分析紀錄列表 |
| 刪除單筆紀錄 | POST | `/record/<int:record_id>/delete` | — | 刪除指定的歷史紀錄，完成後重導向至儀表板 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 (`/`)
- **輸入**：無
- **處理邏輯**：單純渲染首頁視圖。
- **輸出**：渲染 `index.html`。

### 2.2 送出情緒分析 (`/analyze`)
- **輸入**：表單欄位 `user_text` (String, 必填)。
- **處理邏輯**：
  1. 接收 `user_text`。
  2. 呼叫情緒分析模組（或簡單關鍵字比對），得出 `emotion` (正向/負向/中性) 與 `intensity` (強度)。
  3. 根據 `emotion` 產生對應的 `suggestion` (回覆建議)。
  4. 呼叫 Record Model 的 `create` 方法將這些資訊存入資料庫。
- **輸出**：渲染 `result.html`，並將分析結果與建議傳遞給模板顯示。
- **錯誤處理**：若輸入為空字串，Flash 錯誤訊息並重導向回首頁 (`/`)。

### 2.3 歷史紀錄儀表板 (`/dashboard`)
- **輸入**：無
- **處理邏輯**：
  1. 呼叫 Record Model 的 `get_all` 方法取得所有歷史紀錄。
  2. 統計各情緒類別的數量，以供前端 Chart.js 渲染圖表。
- **輸出**：渲染 `dashboard.html`，將歷史列表與統計數據傳遞給模板。

### 2.4 刪除單筆紀錄 (`/record/<record_id>/delete`)
- **輸入**：URL 參數 `record_id` (Integer)。
- **處理邏輯**：呼叫 Record Model 的 `delete(record_id)` 方法。
- **輸出**：重導向至 `/dashboard`。
- **錯誤處理**：若找不到該筆紀錄，回傳 404 Not Found 或 Flash 錯誤並重導向。

---

## 3. Jinja2 模板清單

所有模板皆存放在 `app/templates/` 之下，並繼承自 `base.html`。

1. **`base.html`**：
   - 核心版型，包含 Navbar (導覽列)、Footer 與基礎的 CSS/JS 引入（包含 Chart.js）。
2. **`index.html`** (繼承 `base.html`)：
   - 包含一個 `<form>`，提供 `<textarea>` 讓使用者輸入文字，並有一個送出按鈕。
3. **`result.html`** (繼承 `base.html`)：
   - 顯示該次輸入的文字、分析出的情緒標籤、強度以及社交回覆建議。
   - 提供「回首頁」或「查看儀表板」的按鈕。
4. **`dashboard.html`** (繼承 `base.html`)：
   - 上半部：使用 `<canvas>` 標籤，讓 Chart.js 渲染情緒溫度計與圓餅圖。
   - 下半部：使用 `<table>` 呈現歷史紀錄列表，每筆紀錄後方帶有刪除按鈕 (POST form)。
