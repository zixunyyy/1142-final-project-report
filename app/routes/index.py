from flask import Blueprint, render_template
from app.models import record

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁與文字輸入表單
    
    Returns:
        渲染 index.html 模板
    """
    return render_template('index.html')

@index_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    顯示圖表統計與過去所有的分析紀錄列表
    
    1. 從資料庫取得所有歷史紀錄
    2. 計算各情緒類別統計數量
    3. 傳遞給模板進行 Chart.js 渲染
    
    Returns:
        渲染 dashboard.html 模板
    """
    records = record.get_all()
    
    # 計算情緒統計 (供圖表使用)
    stats = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for r in records:
        emo = r['emotion']
        if emo in stats:
            stats[emo] += 1
        else:
            stats[emo] = 1
            
    return render_template('dashboard.html', records=records, stats=stats)
