from .extensions import socketio, db, user_sid
from flask_socketio import emit
from flask import session, request
from .models import Room, RoomUser, User

@socketio.on("connect")
def handle_connect():
    user_sid[session["username"]] = request.sid

@socketio.on("disconnect")
def handle_disconnect():
    for username in user_sid:
        if user_sid[username] == request.sid:
            del user_sid[username]
            break
    
    session.clear()

@socketio.on("create_room")
def handle_create_room(data):
    room_name = data.get("room_name")
    user_id = data.get("user_id")

    if room_name and user_id:
        new_room = Room(name = room_name, owner_id = user_id)
        db.session.add(new_room)
        db.session.commit()

        add_owner = RoomUser(room_id = new_room.id, user_id = user_id)
        db.session.add(add_owner)
        db.session.commit()

        emit("room_created", {
            "room_name": room_name, 
            "room_id": new_room.id
        }, broadcast=True)

@socketio.on("invite_user")
def handle_invite_user(data):
    from_user_id = data.get("from_user_id")
    room_name = data.get("room_name")
    username = data.get("username")

    if from_user_id and room_name and username:
        user = User.query.filter_by(username = username).first()
        room = Room.query.filter_by(name = room_name).first()

        if user and room:
            already_in = RoomUser.query.filter_by(room_id = room.id, user_id = user.id).first()
            if already_in:
                emit("already_in", {
                    "msg": f"User {username} is already in the room {room.name}"
                }, to=request.sid)
            else:
                try:
                    to_user_sid = user_sid[user.username]
                    emit("invitation", {
                        "from_user": User.query.get(from_user_id).username,
                        "room_name": room.name,
                        "room_id": room.id
                    }, to=to_user_sid)
                except:
                    emit("user_offline", {
                        "msg": f"User {username} is offline"
                    }, to=request.sid)
        else:
            msg = ""
            
            if not user:
                msg += f"User {username} not found\n"
            if not room:
                msg += f"Room {room_name} not found"
            
            emit("user_room_not_found", {
                "msg": msg
            }, to=request.sid)

@socketio.on("add_room")
def handle_add_room(data):
    room_id = data.get("room_id")

    if room_id:
        user = User.query.filter_by(username = session["username"]).first()
        room = Room.query.get(room_id)
        new_user = RoomUser(room_id = room_id, user_id = user.id)
        db.session.add(new_user)
        db.session.commit()

        emit("user_joined", {
            "room_name": room.name, 
            "room_id": room.id
        }, broadcast=True)