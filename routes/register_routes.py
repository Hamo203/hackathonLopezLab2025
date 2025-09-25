import os
import time
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for

import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import json

register_bp = Blueprint("register", __name__, url_prefix="/register")

# --- Firebase初期化 ---
# Web SDK設定（Pyrebase用）

with open("firebase_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Admin SDK (Firestore用)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
#db = firestore.client()

# ルート
@register_bp.route("/", methods=['GET', 'POST'])
def register_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")

        if not email or not password or not username:
            flash("全ての項目を入力してください")
            return render_template("register.html")

        try:
            # Firebase Auth にユーザ作成
            user = auth.create_user_with_email_and_password(email, password)
            uid = user["localId"]

            # Firestoreに追加情報を保存
            db.collection("users").document(uid).set({
                "email": email,
                "username": username,
                "created_at": firestore.SERVER_TIMESTAMP,
            })

            flash("アカウントを作成しました！")
            return redirect(url_for("register.register_page"))

        except Exception as e:
            flash(f"登録に失敗しました: {str(e)}")
            return render_template("register.html")

    return render_template("register.html")
