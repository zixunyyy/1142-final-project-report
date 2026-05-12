from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁與文字輸入表單
    
    Returns:
        渲染 index.html 模板
    """
    pass

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
    pass
