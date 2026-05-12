import sqlite3
from flask import current_app, g

def get_db_connection():
    """
    取得資料庫連線
    使用 flask 的 g 變數來存取當前請求的連線，避免重複建立
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # 讓查詢結果可以用字典 (欄位名稱) 方式取值
        g.db.row_factory = sqlite3.Row
    return g.db
