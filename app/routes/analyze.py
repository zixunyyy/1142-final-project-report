from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.models import record

analyze_bp = Blueprint('analyze', __name__)

def mock_emotion_analysis(text):
    """簡單關鍵字比對的情緒分析邏輯"""
    positive_words = ['好', '快樂', '開心', '棒', '喜歡', '讚', '高興', '幸福']
    negative_words = ['壞', '難過', '生氣', '糟', '討厭', '煩', '氣', '悲傷', '累']
    
    pos_score = sum(1 for word in positive_words if word in text)
    neg_score = sum(1 for word in negative_words if word in text)
    
    if pos_score > neg_score:
        return 'Positive', min(pos_score * 20 + 40, 100), "看起來你的心情不錯！繼續保持這份好心情，並將正能量分享給周圍的人吧。"
    elif neg_score > pos_score:
        return 'Negative', min(neg_score * 20 + 40, 100), "似乎遇到了一些不順心的事情。建議可以深呼吸、稍微休息一下，或者找個信任的朋友聊聊。"
    else:
        return 'Neutral', 50, "這是一段平穩的敘述。也許可以試著多記錄一些細節，幫助自己釐清當下的感受。"

@analyze_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    接收使用者輸入，執行情緒分析並回傳建議結果
    """
    user_text = request.form.get('user_text', '').strip()
    
    if not user_text:
        flash("請輸入想要分析的文字！", "error")
        return redirect(url_for('index.index'))
        
    # 執行簡單情緒分析
    emotion, intensity, suggestion = mock_emotion_analysis(user_text)
    
    data = {
        'user_text': user_text,
        'emotion': emotion,
        'intensity': intensity,
        'suggestion': suggestion
    }
    
    # 儲存紀錄至資料庫
    record_id = record.create(data)
    if not record_id:
        flash("儲存紀錄時發生錯誤。", "error")
        
    return render_template('result.html', data=data)

@analyze_bp.route('/record/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    刪除指定的歷史紀錄
    """
    success = record.delete(record_id)
    if success:
        flash("紀錄已成功刪除！", "success")
    else:
        flash("刪除紀錄時發生錯誤或找不到該筆資料。", "error")
        
    return redirect(url_for('index.dashboard'))
