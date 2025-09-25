import json
import pyrebase
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Flask アプリ作成
app = Flask(__name__, template_folder="../templates")
app.secret_key = "super_secret_key"  # セッション用（適当に変更可）

# Firebase設定を読み込み
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # login_routes.py のあるディレクトリ
config_path = os.path.join(BASE_DIR, "firebase_config.json")

with open(config_path, "r") as f:
    firebase_config = json.load(f)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = user["idToken"]
            flash("ログイン成功しました！", "success")
            return redirect(url_for("index"))
        except Exception as e:
            print("Login error:", e)
            flash("IDかパスワードが異なっています。", "danger")
            return redirect(url_for("login_page"))

    return render_template("login.html")


@app.route("/index")
def index():
    if "user" not in session:
        flash("ログインしてください", "warning")
        return redirect(url_for("login_page"))
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("ログアウトしました", "info")
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(debug=True)
