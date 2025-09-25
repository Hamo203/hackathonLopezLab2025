from flask import Flask
from routes.main_routes import main_bp
from routes.search_routes import search_bp
from routes.login_routes import login_bp
from routes.register_routes import register_bp
from firebase_admin import credentials, firestore
import firebase_admin
#from routes.admin_routes import admin_bp

#比留間追加
import os
from dotenv import load_dotenv

#.envを読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Firebase初期化
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")  # JSON ファイルのパス
cred = credentials.Certificate(cred_path)
if not firebase_admin._apps:   # すでに初期化されている場合はスキップ
    firebase_admin.initialize_app(cred)
db = firestore.client()  # グローバル変数として保持
#ここまで比留間追加

app = Flask(__name__)
app.register_blueprint(main_bp)
app.register_blueprint(search_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
#app.register_blueprint(admin_bp)


if __name__ == "__main__":
    app.run(debug=True)
