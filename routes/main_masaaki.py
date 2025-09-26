import os
from flask import Blueprint, request, jsonify, render_template,current_app,session
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
    print("DEBUG: Accessing /masaaki")
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

@masaaki_bp.route('/api/favorite', methods=["POST"])
def add_favorite():
    db = current_app.config["FIRESTORE_DB"]
    uid = session.get("uid")
    print("DEBUG: uid from session =", uid) 
    if not uid:
        return jsonify({"error": "ログインが必要です"}), 401

    data = request.json
    device_id = data.get("deviceId")
    action = data.get("action")  # "add" or "remove"

    if not device_id:
        return jsonify({"error": "deviceIdが必要です"}), 400

    user_ref = db.collection("users").document(uid)

    if action == "add":
        user_ref.set({
            "favorites": firestore.ArrayUnion([device_id])
        }, merge=True)
    elif action == "remove":
        user_ref.set({
            "favorites": firestore.ArrayRemove([device_id])
        }, merge=True)
    else:
        return jsonify({"error": "不正なactionです"}), 400

    return jsonify({"status": "ok", "action": action, "deviceId": device_id})

if __name__ == "__main__":
    masaaki_bp.run(debug=True)