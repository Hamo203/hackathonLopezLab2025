from flask import Blueprint, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

#firebaseのリストをGPTに送る
import firebase_admin
from firebase_admin import credentials, firestore
#サービスアカウントキーJSONを指定
#cred = credentials.Certificate("serviceAccountKey.json")
#firebase_admin.initialize_app(cred)

#db = firestore.client()
#ここまで


#以下コピペ
import time

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # hackathonLopezLab2025/
#TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

#app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Firebase Admin SDK 初期化
#cred = credentials.Certificate("serviceAccountKey.json")  # FirebaseからDLしたキー
#firebase_admin.initialize_app(cred)
#db = firestore.client()
#以上コdピペ



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

    #Firebaseからデバイス名を取得する
    #device_docs = db.collection("devices").stream()
    #device_names = [doc.to_dict()["name"] for doc in device_docs]

    #追加メッセージ
    additional_prompt = "この質問に対して、研究室にある以下のデバイスの中から最適なものを提案してください:\n"
    #additional_prompt += ", ".join(device_names)

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

    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=data)

    reply = response.json()["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})
