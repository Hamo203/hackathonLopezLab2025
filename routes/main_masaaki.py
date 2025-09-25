import os
from flask import Blueprint, request, jsonify, render_template,current_app
import firebase_admin
from firebase_admin import credentials, firestore
from collections import defaultdict

masaaki_bp = Blueprint("masaaki", __name__, url_prefix="/masaaki")

# Firebase Admin SDK 初期化
#cred = credentials.Certificate("serviceAccountKey.json")  # FirebaseからDLしたキー
#firebase_admin.initialize_app(cred)
#db = firestore.client()


# HTMLを返すルート
@masaaki_bp.route('/')
def masaaki_page():
    db = current_app.config["FIRESTORE_DB"]
    return render_template('masaaki.html')

@masaaki_bp.route('/api/devices')
def get_devices_by_genre():
    db = current_app.config["FIRESTORE_DB"]
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


