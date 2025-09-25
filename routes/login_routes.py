import os
from flask import Blueprint,Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import time

login_bp = Blueprint("login", __name__, url_prefix="/login")

# Firebase Admin SDK 初期化
cred = credentials.Certificate("serviceAccountKey.json")  # FirebaseからDLしたキー
firebase_admin.initialize_app(cred)
db = firestore.client()

# ルート
@login_bp.route("/", methods=['GET', 'POST'])
def login_page():
     return render_template("login.html") 