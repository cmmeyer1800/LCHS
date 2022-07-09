from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from lchs.models import User

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login")
def login():
    return render_template("login.html", next=request.args.get("next"))


@auth.route("/login", methods=["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(f"/auth/login?next={request.args.get('next')}")
    login_user(user, remember=remember)
    next = request.args.get("next")
    if next and not ("None" in next):
        return redirect(request.args.get("next"))
    else:
        return redirect(url_for("main.index"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
