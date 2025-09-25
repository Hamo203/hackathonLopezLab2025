import os
from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # hackathonLopezLab2025/
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Firebase Admin SDK 初期化
#cred = credentials.Certificate("serviceAccountKey.json")  # FirebaseからDLしたキー
#firebase_admin.initialize_app(cred)
#db = firestore.client()


# HTMLを返すルート
@app.route('/')
def index():
    return render_template('masaaki.html')

@app.route('/api/devices')
def get_devices_by_genre():
    docs = db.collection('devices').stream()

    # ジャンルごとにデータをまとめる
    genre_dict = defaultdict(list)
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        genres = data.get('genre', [])  # 配列型のgenre
        if not genres:
            genres = ['未分類']  # genreがない場合
        for g in genres:
            genre_dict[g].append(data)

    return jsonify(genre_dict)

if __name__ == '__main__':
    app.run(debug=True)
