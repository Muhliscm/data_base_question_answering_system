from flask import Flask
from .views import views
from .db import connect_db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "my_key"
    app.register_blueprint(views, url_prefix="/")
    return app
