# app.py
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import time

app = Flask(__name__)

# Firebase Admin SDK 初期化
cred = credentials.Certificate("serviceAccountKey.json")  # FirebaseからDLしたキー
firebase_admin.initialize_app(cred)
db = firestore.client()

# ルート
@app.route("/")
def index():
    return "Flask server for Lab Assets running."

# 備品追加
@app.route("/add_asset", methods=["POST"])
def add_asset():
    data = request.json
    required = ["name", "place", "use"]

    # 必須チェック
    for key in required:
        if not data.get(key):
            return jsonify({"status": "error", "message": f"{key} is required"}), 400

    doc = {
        "name": data["name"],
        "place": data["place"],
        "use": data["use"],
        "article": data.get("article") or None,
        "articleUrl": data.get("articleUrl") or None,
        "updatedAt": int(time.time() * 1000)
    }
    db.collection("assets").add(doc)
    return jsonify({"status": "success", "message": "Asset added"})

# 備品削除（名前検索して最初の1件を削除）
@app.route("/delete_asset", methods=["POST"])
def delete_asset():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"status": "error", "message": "name is required"}), 400

    query = db.collection("assets").where("name", "==", name).stream()
    deleted = 0
    for doc in query:
        db.collection("assets").document(doc.id).delete()
        deleted += 1
        break  # 最初の1件のみ削除
    if deleted == 0:
        return jsonify({"status": "error", "message": "No asset found"}), 404
    return jsonify({"status": "success", "message": f"{name} deleted"})

if __name__ == "__main__":
    app.run(debug=True)
