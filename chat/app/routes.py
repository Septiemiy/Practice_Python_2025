from flask import Blueprint, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import User, Room

registration = Blueprint("registration", __name__)
chat = Blueprint("chat", __name__)

@registration.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if password != None and check_password_hash(user.password, password):
                session["username"] = username
                return redirect("/chat")
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
            session["username"] = username
            return redirect("/chat")

    return render_template("signup.html")

@chat.route("/chat")
def chat_page():
    if "username" not in session:
        return redirect("/")
    
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    owned_rooms = user.owned_rooms
    user_rooms = user.rooms
    room_ids = [room.room_id for room in user_rooms]
    joined_rooms = Room.query.filter(Room.id.in_(room_ids)).all()
    joined_rooms = [room for room in joined_rooms if room not in owned_rooms]

    return render_template("chat.html", owned_rooms = owned_rooms, joined_rooms = joined_rooms, user_id = user.id)

@chat.route("/logout")
def logout():
    return redirect("/")