import json
import pyrebase
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
# Firebase設定を読み込み
from firebase_admin import firestore
import os, json

# Flask アプリ作成
login_bp = Blueprint("login", __name__,url_prefix="/login")

with open("firebase_config.json", "r", encoding="utf-8") as f:
    config = json.load(f) 


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@login_bp.route("/login", methods=["GET", "POST"])
def login_page():
     db = current_app.config["FIRESTORE_DB"]
     if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = user["idToken"]
            flash("ログイン成功しました！", "success")
            return redirect(url_for("search.search_page"))
        except Exception as e:
            print("Login error:", e)
            flash("IDかパスワードが異なっています。", "danger")
            return redirect(url_for("login.login_page"))

     return render_template("login.html")


@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("ログアウトしました", "info")
    return redirect(url_for("login.login_page"))
