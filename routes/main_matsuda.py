import os
from flask import Blueprint, request, jsonify, render_template,current_app
import firebase_admin
from firebase_admin import credentials, firestore
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # hackathonLopezLab2025/
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


matsuda_bp = Blueprint("matsuda", __name__, url_prefix="/matsuda")

# Firebase Admin SDK 初期化
#cred = credentials.Certificate("serviceAccountKey.json")  # FirebaseからDLしたキー
#firebase_admin.initialize_app(cred)
#db = firestore.client()

# ルート
@matsuda_bp.route("/")
def add_page():
    db = current_app.config["FIRESTORE_DB"] 
    return render_template("matsuda.html") 

# 備品追加
@matsuda_bp.route("/add_asset", methods=["POST"])
def add_asset():
    ##################################################################
    #dbにアクセス
    db = current_app.config["FIRESTORE_DB"]
    if db is None:
        return jsonify({"error": "Database not configured"}), 500
    ##################################################################
    data = request.json
    required = ["name", "place", "use"]
    for key in required:
        if not data.get(key):
            return jsonify({"status":"error","message":f"{key} is required"}), 400
    doc = {
        "name": data["name"],
        "place": data["place"],
        "use": data["use"],
        "article": data.get("article") or None,
        "articleUrl": data.get("articleUrl") or None,
        "genres": data.get("genres") or [],  # 🔽 ジャンル追加
        "updatedAt": int(time.time()*1000)
    }
    db.collection("devices").add(doc)
    return jsonify({"status":"success","message":"Asset added to devices"})

# 備品削除（名前検索して最初の1件を削除）
@matsuda_bp.route("/delete_asset", methods=["POST"])
def delete_asset():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"status": "error", "message": "name is required"}), 400

    query = db.collection("devices").where("name", "==", name).stream()
    deleted = 0
    for doc in query:
        db.collection("devices").document(doc.id).delete()
        deleted += 1
        break  # 最初の1件のみ削除
    if deleted == 0:
        return jsonify({"status": "error", "message": "No asset found"}), 404
    return jsonify({"status": "success", "message": f"{name} deleted"})


