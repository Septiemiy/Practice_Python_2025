from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import User

registration = Blueprint('registration', __name__)

@registration.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if password != None and check_password_hash(user.password, password):
                return redirect("/pass")
            else:
                return render_template("login.html", username = username, password_field = True)
        else:
            flash("User doesn`t exists!", "error")
            return render_template("login.html", need_signup = True)

    return render_template("login.html")

@registration.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        exists_user = User.query.filter_by(username=username).first()
        if exists_user:
            flash("User already exists!", "error")
            return render_template("signup.html")
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect("/pass")

    return render_template("signup.html")