from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from .routes import main

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    db = SQLAlchemy()
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(main)

    socketio.init_app(app)

    return app