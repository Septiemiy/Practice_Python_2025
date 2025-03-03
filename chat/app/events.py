from .extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("User connected!")