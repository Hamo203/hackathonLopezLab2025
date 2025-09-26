# search_routes.py

from flask import Blueprint, render_template, request, jsonify, current_app
import os
import requests
from dotenv import load_dotenv
import json # jsonライブラリをインポート

search_bp = Blueprint("search", __name__, url_prefix="/search")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@search_bp.route("/")
def search_page():
    return render_template("search_hiruma.html")

@search_bp.route("/chat", methods=["POST"])
def chat():
    """ユーザー入力に基づいて最適なデバイス情報をFirestoreから取得して返す"""
    db = current_app.config["FIRESTORE_DB"]
    if db is None:
        return jsonify({"error": "Database not configured"}), 500

    user_message = request.json.get("message")

    # Firebaseから全デバイス名を取得
    try:
        device_docs = db.collection("devices").stream()
        device_names = [doc.to_dict()["name"] for doc in device_docs]
    except Exception as e:
        print(f"Error fetching devices from Firestore: {e}")
        return jsonify({"error": f"Firestoreからのデバイス取得に失敗しました: {e}"}), 500

    # ChatGPTへの指示を、デバイス名を返すように変更
    prompt_for_device_names = "以下のリストの中から、この質問に最も適したデバイスの名前だけをカンマ区切りで挙げてください。他の説明は一切不要です。\n"
    prompt_for_device_names += "デバイスリスト: " + ", ".join(device_names)
    full_message = user_message + "\n" + prompt_for_device_names

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "あなたは研究支援のアシスタントです。ユーザーの質問に最適なデバイス名をリストから選び、カンマ区切りで出力します。"},
            {"role": "user", "content": full_message}
        ]
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, json=data)
        response.raise_for_status()
        # ChatGPTの応答からデバイス名の文字列を取得
        suggested_names_str = response.json()["choices"][0]["message"]["content"]
        # カンマで分割し、前後の空白を削除してリスト化
        suggested_names = [name.strip() for name in suggested_names_str.split(',')]
        
        if not suggested_names or suggested_names == ['']:
             return jsonify([]) # 提案がない場合は空のリストを返す

        # 提案された名前のデバイス情報をFirestoreから取得
        suggested_devices = []
        # Firestoreの `in` クエリは最大30個の要素までなので、必要に応じて分割処理が必要
        # ここでは簡単のため、30個以下を想定
        if suggested_names:
            docs = db.collection('devices').where('name', 'in', suggested_names).stream()
            for doc in docs:
                device_data = doc.to_dict()
                device_data['id'] = doc.id # ドキュメントIDも追加
                suggested_devices.append(device_data)
        
        return jsonify(suggested_devices)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {e}"}), 500
    except (KeyError, IndexError):
        return jsonify({"error": "Invalid response from OpenAI API"}), 500