from flask import Blueprint, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

search_bp = Blueprint("search", __name__, url_prefix="/search")

# .env読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)


@search_bp.route("/")
def search_page():
    return render_template("search_hiruma.html")


@search_bp.route("/chat", methods=["POST"])
def chat():
    """ユーザー入力を受け取り、ChatGPT APIを呼び出して返答を返す"""
    user_message = request.json.get("message")
    #追加メッセージ
    user_message += "ツンデレでしゃべって"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "あなたは研究支援のアシスタントです。"},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=data)

    reply = response.json()["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})
