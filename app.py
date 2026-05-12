import os
import sqlite3
from flask import Flask, g
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 專案設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 資料庫連線釋放處理
    @app.teardown_appcontext
    def close_db(error):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    # 註冊路由 Blueprints
    from app.routes.index import index_bp
    from app.routes.analyze import analyze_bp
    
    app.register_blueprint(index_bp)
    app.register_blueprint(analyze_bp)
    
    return app

app = create_app()

def init_db():
    """初始化資料庫 (用於執行 python -c 'from app import init_db; init_db()')"""
    with app.app_context():
        db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        with app.open_resource('database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
        print("Initialized the database.")

if __name__ == '__main__':
    app.run(debug=True)
