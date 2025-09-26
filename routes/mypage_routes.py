from flask import Blueprint, render_template

mypage_bp = Blueprint("mypage", __name__, url_prefix="/mypage")

@mypage_bp.route("/my_page")
def mypage_page():
    return render_template("mypage.html")
