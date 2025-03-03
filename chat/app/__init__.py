from flask import Flask
from .routes import registration
from .events import socketio
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(registration)

    socketio.init_app(app)

    return app