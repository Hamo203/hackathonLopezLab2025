from flask import Blueprint, render_template, current_app, session, redirect, url_for, flash

mypage_bp = Blueprint("mypage", __name__, url_prefix="/mypage")

# マイページ（お気に入り一覧）
@mypage_bp.route("/")
def mypage_page():
    db = current_app.config["FIRESTORE_DB"]
    uid = session.get("uid")

    if not uid:
        flash("ログインが必要です", "warning")
        return redirect(url_for("login.login_page"))

    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()
    favorites_list = []
    if user_doc.exists:
        data = user_doc.to_dict()
        favorite_ids = data.get("favorites", [])

        for device_id in favorite_ids:
            device_doc = db.collection("devices").document(device_id).get()
            if device_doc.exists:
                d = device_doc.to_dict()
                d["id"] = device_id
                favorites_list.append(d)

    return render_template("mypage.html", favorites=favorites_list)


# お気に入り解除
@mypage_bp.route("/remove/<device_id>", methods=["POST"])
def remove_favorite(device_id):
    db = current_app.config["FIRESTORE_DB"]
    uid = session.get("uid")

    if not uid:
        flash("ログインが必要です", "warning")
        return redirect(url_for("login.login_page"))

    user_ref = db.collection("users").document(uid)
    user_ref.update({
        "favorites": firestore.ArrayRemove([device_id])
    })

    flash("お気に入りを解除しました", "info")
    return redirect(url_for("mypage.favorites_page"))