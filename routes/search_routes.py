from flask import Blueprint, render_template, request, jsonify, current_app #current_app追記
import os
import requests
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import time


search_bp = Blueprint("search", __name__, url_prefix="/search")

# .env読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)#デバック用確認出力


@search_bp.route("/")
def search_page():
    return render_template("search_hiruma.html")


@search_bp.route("/chat", methods=["POST"])
def chat():
    """ユーザー入力を受け取り、ChatGPT APIを呼び出して返答を返す"""


    ##################################################################
    #dbにアクセス
    db = current_app.config["FIRESTORE_DB"]
    if db is None:
        return jsonify({"error": "Database not configured"}), 500
    ##################################################################


    user_message = request.json.get("message")


    ##################################################################
    #Firebaseからデバイス名を取得
    try:
        device_docs = db.collection("devices").stream()
        device_names = [doc.to_dict()["name"] for doc in device_docs]
    except Exception as e:
        print(f"Error fetching devices from Firestore: {e}")
        device_names = []
    ##################################################################

    #追加メッセージ
    additional_prompt = "この質問に対して、研究室にある以下のデバイスの中から最適なものを提案してください:\n"
    additional_prompt += ", ".join(device_names)

    full_message = user_message + "\n" + additional_prompt


    #chatGPTにメッセージを送信する
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "あなたは研究支援のアシスタントです。"},
            {"role": "user", "content": full_message}
        ]
    }


    """
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=data)

    reply = response.json()["choices"][0]["message"]["content"]
    """

    ################################################################################
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, json=data)
        response.raise_for_status() # エラーレスポンスをチェック
        reply = response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {e}"}), 500
    except KeyError:
        return jsonify({"error": "Invalid response from OpenAI API"}), 500
    #################################################################################

    return jsonify({"reply": reply})
