import os
from flask import Blueprint,Flask, request, jsonify, render_template

import time

register_bp = Blueprint("register", __name__, url_prefix="/register")

# ルート
@register_bp.route("/", methods=['GET', 'POST'])
def register_page():
     return render_template("register.html") 