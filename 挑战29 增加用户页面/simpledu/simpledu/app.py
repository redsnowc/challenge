from flask import Flask
from simpledu.config import configs
from simpledu.models import db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    from .handlers import front, course, admin, user
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(user)
