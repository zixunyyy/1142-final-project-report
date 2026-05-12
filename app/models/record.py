from app.models.db import get_db_connection
import sqlite3

def create(data):
    """
    新增一筆情緒紀錄
    
    參數:
        data (dict): 包含 user_text, emotion, intensity, suggestion 等欄位的字典
    回傳:
        int: 新增紀錄的 ID，若失敗則回傳 None
    """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            '''
            INSERT INTO records (user_text, emotion, intensity, suggestion)
            VALUES (?, ?, ?, ?)
            ''',
            (data.get('user_text'), data.get('emotion'), data.get('intensity'), data.get('suggestion'))
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error in create: {e}")
        return None

def get_all():
    """
    取得所有情緒紀錄
    
    回傳:
        list: 包含所有紀錄的 sqlite3.Row 物件列表
    """
    try:
        db = get_db_connection()
        records = db.execute('SELECT * FROM records ORDER BY created_at DESC').fetchall()
        return records
    except sqlite3.Error as e:
        print(f"Database error in get_all: {e}")
        return []

def get_by_id(record_id):
    """
    取得單筆情緒紀錄
    
    參數:
        record_id (int): 紀錄 ID
    回傳:
        sqlite3.Row: 單筆紀錄物件，若找不到則回傳 None
    """
    try:
        db = get_db_connection()
        record = db.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
        return record
    except sqlite3.Error as e:
        print(f"Database error in get_by_id: {e}")
        return None

def update(record_id, data):
    """
    更新一筆情緒紀錄
    
    參數:
        record_id (int): 要更新的紀錄 ID
        data (dict): 要更新的欄位與值
    回傳:
        bool: 更新是否成功
    """
    try:
        db = get_db_connection()
        db.execute(
            '''
            UPDATE records 
            SET user_text = ?, emotion = ?, intensity = ?, suggestion = ?
            WHERE id = ?
            ''',
            (data.get('user_text'), data.get('emotion'), data.get('intensity'), data.get('suggestion'), record_id)
        )
        db.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error in update: {e}")
        return False

def delete(record_id):
    """
    刪除一筆情緒紀錄
    
    參數:
        record_id (int): 要刪除的紀錄 ID
    回傳:
        bool: 刪除是否成功
    """
    try:
        db = get_db_connection()
        db.execute('DELETE FROM records WHERE id = ?', (record_id,))
        db.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error in delete: {e}")
        return False
